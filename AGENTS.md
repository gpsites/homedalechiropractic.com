# Site maintenance

This is a plain static HTML, CSS, and JavaScript site. Keep the deployed pages self-contained and do not add a runtime framework, CMS, or client-side HTML includes.

The shared page chrome has canonical sources:

- `partials/header.html` — announcement bar, logo, and main navigation
- `partials/footer.html` — visit band, contact details, and footer navigation
- `partials/brand.html` — logo shared by the header and footer

Never hand-edit markup between the `shared-header` or `shared-footer` comments in an HTML page. Edit the appropriate partial, then run:

```sh
make stitch
make check
```

If `make` is unavailable, run `python3 scripts/sync-shared.py` and `python3 scripts/sync-shared.py --check` directly. The sync script resolves each page’s relative links and `aria-current` state, then updates the CSS and JavaScript cache-busting hashes from their current contents. Commit the partials, sync script, and synchronized HTML together. Before publishing, also run `git diff --check` and `node --check assets/site.js`.

For local preview with automatic reloads, run `make serve` (or `python3 scripts/preview.py`). The server injects its reload helper into HTTP responses only; never add development reload code to the site files.

GitHub Pages publishes the `gh-pages` branch. Never force-push.
