# GitHub Pages Pipeline

This directory contains the GitHub Pages deployment workflow for this repository.

## File

- `.github/workflows/pages.yml`: deploys the repository root as the GitHub Pages site.

## Purpose

Deploy the repository root directly to GitHub Pages. No frontend build step is required; static files are served as-is.

## Triggers

- `push` to `main`
- `workflow_dispatch` (manual run from Actions tab)

## Steps in order

1. **Checkout**: `actions/checkout@v4` checks out the repository.
2. **Configure Pages**: `actions/configure-pages@v5` prepares the Pages environment.
3. **Upload artifact**: `actions/upload-pages-artifact@v3` uploads the repository root (`.`) as the Pages artifact.
4. **Deploy**: `actions/deploy-pages@v4` deploys the artifact to `https://bniladridas.github.io/`.

## Assumptions that should not be changed casually

- The repository root is the Pages source. Do not wrap the site in a subdirectory like `Site/` or change `path: "."` without updating all related paths.
- `index.html` is at the repository root.
- `content/about.json` is part of the deployed site and is fetched by `script.js` at runtime.
- `admin/` is deployed as part of the static site at `https://bniladridas.github.io/admin/`.
- `.nojekyll` is present so `.github/`, `admin/`, and `content/` are served.
- The Python package build is separate from Pages; `pyproject.toml` `force-include` maps `Site` files into the wheel but Pages serves the repository root directly.

## Inspecting a failed run

1. Open `https://github.com/bniladridas/bniladridas.github.io/actions`
2. Select the failed `Deploy to GitHub Pages` run.
3. Expand the failed step and read the logs.

## Verify after deployment

- `https://bniladridas.github.io/`: homepage
- `https://bniladridas.github.io/content/about.json`: About JSON
- `https://bniladridas.github.io/admin/`: Decap CMS (requires OAuth to edit)
- `https://bniladridas.github.io/assets/thumbnail.png` and `https://bniladridas.github.io/og-image.png`: assets

## Distinction

- **GitHub Pages** deploys the repository root via this workflow.
- **Python wheel** is built via `pyproject.toml` `hatchling` and is unrelated to Pages. Publishing to PyPI is separate.

Decap CMS authentication is a separate configuration concern from this deployment pipeline.
