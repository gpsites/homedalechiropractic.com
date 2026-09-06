# Homedale Chiropractic

A plain HTML, CSS, and JavaScript website for Dr J Edward Perkins. No framework, package installation, CMS, or production build step is required.

## Preview

From this directory, run:

```sh
make serve
```

Open http://127.0.0.1:4173. The preview server synchronizes shared partial changes and reloads open pages when HTML, CSS, JavaScript, or image files change. Its reload helper is injected only into local HTTP responses; no development code is written into the site or deployed.

The Makefile is only a convenience layer. The equivalent command is `python3 scripts/preview.py`.

## Edit

Edit page-specific content directly in the HTML pages. Each deployed page remains a complete, standalone HTML document:

- `index.html`: home page and photo carousel.
- `about/index.html`: biography, education, family, team members, and photo gallery.
- `chiropractic/index.html`: adjusting techniques and physiotherapeutics.
- `naturopathic/index.html`: nutritional therapies and injection therapies.
- `GPA/index.html`: Gravitational Pattern Alignment.
- `atlas/index.html`: complete Atlas booklet with chapter navigation.
- `promise/index.html`: patient promise.
- `contact/index.html`: address, phone, office hours, and map.

Shared assets:

- `assets/site.css`: typography, layout, responsive styles, and print styles.
- `assets/site.js`: mobile menu, carousel, and photo viewer; content remains available without JavaScript.
- `assets/photos/`: photographs and illustrations with descriptive filenames. Files ending in `-retouched.webp` are AI-edited derivatives.
- `assets/fonts/`: locally hosted fonts and their licenses.
- `assets/three-fingers.svg`: standalone logo; its inline copies appear in page headers and footers.
- `assets/favicon.svg`: browser icon.

Shared markup:

- `partials/header.html`: announcement bar, logo, and primary navigation.
- `partials/footer.html`: call-to-action band, contact details, and footer navigation.
- `partials/brand.html`: logo markup used by both shared partials.
- `scripts/sync-shared.py`: mechanically copies the partials into every page, resolves relative paths and current-page navigation state, and updates CSS/JavaScript cache-busting hashes from the current file contents. It uses only the Python 3 standard library.
- `scripts/preview.py`: standard-library local server with automatic partial synchronization and browser reloads.

After changing a partial, synchronize and verify the pages:

```sh
make stitch
make check
```

The synchronizer deliberately uses conservative Python syntax and long-established standard-library modules. It requires no packages, installation, or network access and is tested on both macOS and Linux. `make check` also reports stale cache-busting hashes.

Without `make`, run `python3 scripts/sync-shared.py` and `python3 scripts/sync-shared.py --check` directly.

Do not edit between the `shared-header` or `shared-footer` comments in a page; those generated regions carry an inline `DO NOT EDIT HERE` warning and are replaced by the sync script. Keep sitemap entries in sync with page URLs.

## Hosting

The site uses GitHub Pages and the existing `CNAME`. Existing page URLs are preserved, including uppercase `/GPA/`; the two service pages have their own URLs. The only external embed is Google Maps on the contact page; fonts and other assets are local.

Before deployment, run:

```sh
make stitch
make check
git diff --check
```

Commit the canonical partials and synchronized HTML pages together, then publish the commit to `gh-pages` with a normal push. Never force-push.

Work is being reviewed locally on `codex/modern-redesign`. Do not push or publish before the user approves the design. Never force-push.
