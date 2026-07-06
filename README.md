# Palmshed

Thoughtful engineering, honest evaluation, enduring craft.

## What this is

Palmshed publishes careful observations from sustained work with software and tools. The primary content is a set of reviews of CLI AI coding agents, each documenting what a tool does, where it succeeds, where it falls short, and where it sits in its development. The aim is truthful observation, not advocacy.

16 agents are reviewed across three classifications:

- **Active** – used regularly in daily work; reviews are current and maintained
- **Occasional** – evaluated periodically; limited applicability or early maturity
- **Archived** – observations from past use; preserved for reference

## Architecture

Pure static site on GitHub Pages. No frameworks, no JavaScript framework, no build tool beyond Python stdlib.

- 26 HTML pages, all hand-authored
- `data.js` – handwritten canonical org data (id, status, order, addedDate)
- `build.py` – generates `agents.js`, `search-index.json`, `rss.xml`, `sitemap.xml` in one command
- Agent HTML pages own their own review metadata (name, developer, version, dates)
- Client-side search with keyboard nav, highlighting, and `/` focus
- GitHub OAuth sign-in via Cloudflare Worker (token exchange, no client secret in repo)
- RSS feed, XML sitemap, `robots.txt`, `404.html`

## Design

Calm, text-first, built to disappear so the writing leads. Details in `PHILOSOPHY.md`.

- Vertical right navigation on desktop, hamburger menu on mobile
- Keyboard shortcuts panel as a floating reference card (no backdrop)
- Alt/Option reveals hidden navigation key hints
- En dashes, no em dashes, no emojis, no marketing copy
- All transitions under 150ms; respects `prefers-reduced-motion`
- Touch targets ≥ 44px; semantic HTML throughout

## Build

```sh
python3 build.py
```

Generates `agents.js`, `search-index.json`, `rss.xml`, `sitemap.xml` from `data.js` and agent HTML pages. Run after adding a new agent or updating a review.

## Adding an agent

1. Create `agents/<id>/index.html` following the existing review template
2. Add an entry to `data.js`
3. Run `python3 build.py`

No redesign needed.

## Developer

Niladri Das – sole developer, writer, and maintainer.

## License

The code is MIT. The writing is not – reviews and essays are copyrighted.

&copy; 2026 Niladri Das. Published under the Palmshed identity.
