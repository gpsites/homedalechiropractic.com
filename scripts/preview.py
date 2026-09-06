#!/usr/bin/env python3

"""Serve the site locally with automatic partial syncing and page reloads."""

import argparse
import email.utils
import io
import os
import subprocess
import sys
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote, urlsplit


SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNC_SCRIPT = os.path.join(SITE_ROOT, "scripts", "sync-shared.py")
WATCHED_EXTENSIONS = (
    ".css",
    ".html",
    ".jpeg",
    ".jpg",
    ".js",
    ".pdf",
    ".png",
    ".svg",
    ".webp",
)
RELOAD_SCRIPT = b"""<script>
(function () {
  var knownVersion = null;
  function checkForChanges() {
    fetch('/__dev_version', { cache: 'no-store' })
      .then(function (response) { return response.text(); })
      .then(function (version) {
        if (knownVersion !== null && version !== knownVersion) {
          window.location.reload();
        }
        knownVersion = version;
      })
      .catch(function () {});
  }
  checkForChanges();
  window.setInterval(checkForChanges, 750);
}());
</script>
"""


def synchronize():
    subprocess.check_call([sys.executable, SYNC_SCRIPT], cwd=SITE_ROOT)


def latest_version():
    latest = 0
    for directory, names, filenames in os.walk(SITE_ROOT):
        names[:] = [name for name in names if name != ".git"]
        for filename in filenames:
            if not filename.lower().endswith(WATCHED_EXTENSIONS):
                continue
            path = os.path.join(directory, filename)
            latest = max(latest, os.stat(path).st_mtime_ns)
    return str(latest)


def partials_version():
    latest = os.stat(SYNC_SCRIPT).st_mtime_ns
    partials = os.path.join(SITE_ROOT, "partials")
    for filename in os.listdir(partials):
        path = os.path.join(partials, filename)
        if os.path.isfile(path):
            latest = max(latest, os.stat(path).st_mtime_ns)
    return latest


class PreviewHandler(SimpleHTTPRequestHandler):
    last_partials_version = None

    def do_GET(self):
        self.synchronize_if_needed()
        path = urlsplit(self.path).path

        if path == "/__dev_version":
            self.send_version()
            return

        local_path = self.translate_path(unquote(path))
        if os.path.isdir(local_path):
            if not path.endswith("/"):
                SimpleHTTPRequestHandler.do_GET(self)
                return
            local_path = os.path.join(local_path, "index.html")

        if local_path.endswith(".html") and os.path.isfile(local_path):
            self.send_html(local_path)
            return

        SimpleHTTPRequestHandler.do_GET(self)

    def synchronize_if_needed(self):
        version = partials_version()
        if version == self.__class__.last_partials_version:
            return
        synchronize()
        self.__class__.last_partials_version = version

    def send_version(self):
        content = latest_version().encode("ascii")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_html(self, path):
        with io.open(path, "rb") as handle:
            content = handle.read()
        content = content.replace(b"</body>", RELOAD_SCRIPT + b"</body>")
        modified = os.stat(path).st_mtime

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Last-Modified", email.utils.formatdate(modified, usegmt=True))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bind", default="127.0.0.1", help="address to bind")
    parser.add_argument("--port", type=int, default=4173, help="port to use")
    arguments = parser.parse_args()

    synchronize()
    PreviewHandler.last_partials_version = partials_version()
    os.chdir(SITE_ROOT)
    server = HTTPServer((arguments.bind, arguments.port), PreviewHandler)
    url = "http://" + arguments.bind + ":" + str(arguments.port)
    sys.stdout.write("Previewing " + url + " with automatic reloads\n")
    sys.stdout.flush()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
