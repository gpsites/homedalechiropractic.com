# Homedale Chiropractic

A plain HTML, CSS, and JavaScript website for Dr J Edward Perkins. No framework, package installation, CMS, or production build step is required.

## Preview

From this directory, run:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173.

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
- `scripts/sync-shared.sh`: mechanically copies the partials into every page, resolving relative paths and the current-page navigation state. It uses only POSIX shell and standard utilities available on macOS and Linux.

After changing a partial, synchronize and verify the pages:

```sh
./scripts/sync-shared.sh
./scripts/sync-shared.sh --check
```

The synchronizer requires only POSIX `/bin/sh` and standard command-line utilities. It is tested on macOS and in Alpine Linux 3.20 using BusyBox. No Python, Node.js, package installation, or network access is required to synchronize the HTML.

Do not edit between the `shared-header` or `shared-footer` comments in a page; those regions are replaced by the sync script. Keep sitemap entries in sync with page URLs.

## Hosting

The site uses GitHub Pages and the existing `CNAME`. Existing page URLs are preserved, including uppercase `/GPA/`; the two service pages have their own URLs. The only external embed is Google Maps on the contact page; fonts and other assets are local.

Before deployment, run:

```sh
./scripts/sync-shared.sh
./scripts/sync-shared.sh --check
git diff --check
```

Commit the canonical partials and synchronized HTML pages together, then publish the commit to `gh-pages` with a normal push. Never force-push.

Work is being reviewed locally on `codex/modern-redesign`. Do not push or publish before the user approves the design. Never force-push.
