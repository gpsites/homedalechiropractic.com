# Homedale Chiropractic

A plain HTML, CSS, and JavaScript website for Dr J Edward Perkins. No framework, package installation, CMS, or build step is required.

## Preview

From this directory, run:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173.

## Edit

Edit the HTML pages directly. Each page contains its complete content, navigation, and footer:

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

When changing shared header or footer content, update all nine pages. Keep sitemap entries in sync with page URLs.

## Hosting

The site uses GitHub Pages and the existing `CNAME`. Existing page URLs are preserved, including uppercase `/GPA/`; the two service pages have their own URLs. The only external embed is Google Maps on the contact page; fonts and other assets are local.

Work is being reviewed locally on `codex/modern-redesign`. Do not push or publish before the user approves the design. Never force-push.
