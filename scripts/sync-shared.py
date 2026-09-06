#!/usr/bin/env python3

"""Copy the shared header and footer partials into every static HTML page."""

import argparse
import hashlib
import io
import os
import re
import sys


SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIALS_DIR = os.path.join(SITE_ROOT, "partials")
PAGES = (
    ("index.html", "", "home"),
    ("chiropractic/index.html", "../", "chiropractic"),
    ("naturopathic/index.html", "../", "naturopathic"),
    ("GPA/index.html", "../", "gpa"),
    ("atlas/index.html", "../", "atlas"),
    ("promise/index.html", "../", "promise"),
    ("about/index.html", "../", "about"),
    ("contact/index.html", "../", "contact"),
)
NAV_KEYS = tuple(page[2] for page in PAGES)
HASHED_ASSETS = ("assets/site.css", "assets/site.js")


def read_text(path):
    with io.open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def write_text(path, content):
    temporary_path = path + ".sync-temp"
    try:
        with io.open(temporary_path, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        os.replace(temporary_path, path)
    finally:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)


def content_hash(relative_path):
    digest = hashlib.sha256()
    path = os.path.join(SITE_ROOT, relative_path)
    with io.open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()[:12]


def update_asset_hashes(source, hashes, relative_path):
    for asset in HASHED_ASSETS:
        pattern = re.escape(asset) + r"\?v=[0-9a-f]+"
        replacement = asset + "?v=" + hashes[asset]
        source, count = re.subn(pattern, replacement, source)
        if count != 1:
            raise ValueError(
                relative_path
                + " should contain exactly one cache-busted reference to "
                + asset
            )
    return source


def render(template_name, root, current):
    template = read_text(os.path.join(PARTIALS_DIR, template_name))
    brand = read_text(os.path.join(PARTIALS_DIR, "brand.html")).strip()
    result = template.replace("{{brand}}", brand)
    result = result.replace("{{root}}", root)

    for key in NAV_KEYS:
        token = "{{" + key + "-current}}"
        value = ' aria-current="page"' if key == current else ""
        result = result.replace(token, value)

    if "{{" in result or "}}" in result:
        raise ValueError("Unresolved token in " + template_name)

    return result.strip()


def make_block(kind, content):
    lines = []
    lines.append(
        "    <!-- shared-"
        + kind
        + ":start; GENERATED - DO NOT EDIT HERE; edit partials/"
        + kind
        + ".html and run python3 scripts/sync-shared.py -->"
    )
    for line in content.splitlines():
        lines.append("    " + line if line else "")
    lines.append("    <!-- shared-" + kind + ":end -->")
    return "\n".join(lines)


def replace_block(page, kind, replacement):
    start_marker = (
        "    <!-- shared-"
        + kind
        + ":start; GENERATED - DO NOT EDIT HERE; edit partials/"
        + kind
        + ".html and run python3 scripts/sync-shared.py -->"
    )
    end_marker = "    <!-- shared-" + kind + ":end -->"

    start = page.find(start_marker)
    if start == -1:
        raise ValueError("Missing " + kind + " start marker")

    end = page.find(end_marker, start)
    if end == -1:
        raise ValueError("Missing " + kind + " end marker")

    end += len(end_marker)
    return page[:start] + replacement + page[end:]


def synchronized_source(path, root, current, hashes, relative_path):
    source = read_text(path)
    header = make_block("header", render("header.html", root, current))
    footer = make_block("footer", render("footer.html", root, current))
    synchronized = replace_block(source, "header", header)
    synchronized = replace_block(synchronized, "footer", footer)
    return update_asset_hashes(synchronized, hashes, relative_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report out-of-sync pages without changing files",
    )
    arguments = parser.parse_args()

    hashes = {}
    for asset in HASHED_ASSETS:
        hashes[asset] = content_hash(asset)

    drifted = []
    for relative_path, root, current in PAGES:
        path = os.path.join(SITE_ROOT, relative_path)
        source = read_text(path)
        synchronized = synchronized_source(
            path, root, current, hashes, relative_path
        )
        if source == synchronized:
            continue
        drifted.append(relative_path)
        if not arguments.check:
            write_text(path, synchronized)

    if arguments.check and drifted:
        sys.stderr.write("Shared markup is out of sync:\n")
        for relative_path in drifted:
            sys.stderr.write("  " + relative_path + "\n")
        sys.stderr.write("Run: python3 scripts/sync-shared.py\n")
        return 1

    action = "Checked" if arguments.check else "Synchronized"
    sys.stdout.write(action + " " + str(len(PAGES)) + " pages.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
