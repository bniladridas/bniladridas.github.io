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
