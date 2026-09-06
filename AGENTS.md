# Site maintenance

This is a plain static HTML, CSS, and JavaScript site. Keep the deployed pages self-contained and do not add a runtime framework, CMS, or client-side HTML includes.

The shared page chrome has canonical sources:

- `partials/header.html` — announcement bar, logo, and main navigation
- `partials/footer.html` — visit band, contact details, and footer navigation
- `partials/brand.html` — logo shared by the header and footer

Never hand-edit markup between the `shared-header` or `shared-footer` comments in an HTML page. Edit the appropriate partial, then run:

```sh
./scripts/sync-shared.sh
./scripts/sync-shared.sh --check
```

The sync script resolves each page’s relative links and `aria-current` state. Commit the partials, sync script, and synchronized HTML together. Before publishing, also run `git diff --check` and `node --check assets/site.js`.

GitHub Pages publishes the `gh-pages` branch. Never force-push.
