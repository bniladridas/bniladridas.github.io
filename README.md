<p align="center">
  <img src="https://raw.githubusercontent.com/bniladridas/bniladridas.github.io/main/.github/assets/thumbnail.png" alt="portfolio" width="100%">
</p>

# bniladridas-portfolio

Portfolio server for bniladridas: **Traction** and **Palmshed Sandbox**.

Live site: https://bniladridas.github.io/

## Install

```bash
pip install bniladridas-portfolio
```

## Use

```bash
portfolio serve
portfolio serve --port 8000 --open
python -m bniladridas_portfolio.cli serve --host 127.0.0.1 --port 8000
```

Serves the same static site that GitHub Pages serves.

## Edit About

The About section at `content/about.json` is editable from the site via Decap CMS at `https://bniladridas.github.io/admin/` (GitHub login required, admin only). Edits are saved as Git commits to `main`.

## Project structure

* `index.html`, `script.js`, `styles.css`: static portfolio source
* `content/about.json`: editable About content
* `admin/`: Decap CMS interface and configuration (`admin/config.yml`)
* `assets/`: site assets (`og-image.png`, `thumbnail.png`)
* `src/bniladridas_portfolio/`: Python package and CLI (`portfolio serve`)
* `tests/e2e/`: browser and site regression tests
* `.github/workflows/pages.yml`: GitHub Pages deployment
* `verify-human.py`: human-feel and site quality checks

The repository root is intentionally both the project root and the GitHub Pages source.

## Development

For serving the portfolio locally, see the commands in the Use section above.

```bash
npm run test:e2e
python3 verify-human.py
```

`portfolio serve` serves the repository root. `npm run test:e2e` runs the jsdom E2E suite. `verify-human.py` checks human-feel, visual noise, and live asset reachability.

## Deployment

Pushes to `main` trigger the GitHub Pages workflow. The repository root is deployed directly. See `.github/workflows/README.md` for the detailed pipeline.

## Packaging

`pyproject.toml` packages the static site into the Python wheel via `force-include`, mapping `index.html`, `styles.css`, `script.js`, `og-image.png`, `assets`, `content`, and `admin` into `bniladridas_portfolio/static/`. GitHub Pages serves the repository root directly; the wheel is built separately.

## Content editing

About content lives in `content/about.json` and is loaded by the site. `/admin/` is the CMS entry point. GitHub OAuth authentication for Decap is a separate configuration concern.

## Project Journey

This repository's architecture, security decisions, debugging history, and SDK roadmap are documented in the public project journey Gist.

[Read the full project journey](https://gist.github.com/bniladridas/88efa3afa553187692f0d45a45c262c8)
