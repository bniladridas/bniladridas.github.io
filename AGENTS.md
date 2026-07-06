# Palmshed — Project Summary

## Goal
Design and maintain a calm, reading-first static site with optional auth and client-side search. The interface should disappear so writing becomes the focus.

## Constraints & Preferences
- Always possible to read without signing in; accounts are optional convenience, not access
- GitHub is the preferred sign-in method; email auth is stubbed for later
- No marketing copy, illustrations, or promotional messages on the auth page
- Search must be client-side, index all pages, support `/` focus, keyboard nav, highlighting, instant results
- No tracking queries, no ads, respect privacy; search should feel like a personal notebook
- Prefer en dashes (–) over em dashes (—)
- Navigation should be calm, not visually dominant; keyboard hints hidden by default; search like an invitation, not an item
- The interface is now stable; future changes should begin with "Does this improve understanding?"
- Avoid redesigns, avoid chasing design trends
- Prioritize better writing, better engineering, better accessibility, better documentation, better observations
- After a reader found that Option on Mac activates Alt hints, document it instead of changing the trigger

## Design Direction
The interface has crossed a threshold from making things quieter to making the interface disappear. The shortcuts panel now floats with no backdrop — it rests on the page like a notebook page rather than interrupting it. Any future change should make it simpler, not richer.

## Progress

### Done
- Created `auth.js` with stable `window.Auth` API (`getUser`, `isSignedIn`, `signIn`, `signOut`, `_setUser`, `init`)
- Created `/auth/index.html` sign-in page with GitHub OAuth button, email buttons (stubbed)
- Created `/auth/callback/index.html` OAuth callback handler with CSRF state validation and open redirect protection
- Created `workers/auth-worker.js` Cloudflare Worker for code→token exchange (deployed)
- Set `GITHUB_CLIENT_SECRET` as encrypted Cloudflare env var via `wrangler secret put`
- Added auth link, `auth.js` script, sitemap entry to all 22 HTML pages
- Created `search.js` – inline nav search with dropdown, highlighting, keyboard nav, `/` to focus
- Created `/search/index.html` static fallback page for JS-off access
- Restructured nav into three groups (`.nav-left`, `.nav-center`, `.nav-right`) on all 25 pages
- Replaced all em dashes (—) with en dashes (–) site-wide
- Calmed language across all agent pages: removed "Best for…" → "Suitable for…", softened claims
- Ethos page H1 changed from "The Workshop" to "Ethos" to match nav label; intro line updated to bridge the concept
- "All Agents" → "Agents" across all pages, breadcrumbs, nav, search index, script references
- All transitions reduced to ≤ 150ms (mostly 0.08s–0.12s); no scaling or movement on hover
- Keyboard hints (`nav-key-hint`) hidden by default; revealed only on Alt/Option press
- About page rewritten as purpose statement (4 paragraphs, no biography)
- Ethos page rewritten from first principles: Patience, Integrity, Understanding, Humility, Stewardship
- Review template designed: 8 sections with Review context box and evidence traceability
- All 16 agent pages rewritten using new template – Active (OpenCode, Antigravity, Codex), Occasional (Gemini CLI, Claude Code, Aider), Archived (Warp, Cursor, Continue, Goose, OpenHands, Cline, Roo Code, Amp, Crush, Qwen Code)
- `styles.css` – Added `.review-context`, `.review-note`, `.archived-notice` styles
- **Architectural refactor: canonical data model** — `data.js` now owns site organization only (id, status, order, addedDate); all review metadata (name, developer, version, dates) extracted from agent HTML pages by `build.py`
- **`build.py` replaces `build-index.py`** — generates `agents.js` (merged runtime data), `search-index.json`, `rss.xml`, `sitemap.xml` from a single command: `python3 build.py`
- **`agents.js`** — generated runtime file with merged org data + extracted HTML metadata; loaded by Home and Agents pages instead of `data.js`
- **Status-based rendering** — `script.js` now renders ranking and table by status groups (Active → Occasional → Archived) using `a.status` instead of old `a.verdict`; `verdictClass()` replaced with `statusClass()`
- **Developer field added** to all 6 Active/Occasional agent pages' `agent-meta` for consistent extraction
- **`extract_meta()` bug fixed** — now properly handles apostrophes in meta descriptions (was truncating at "Cloud's")
- **Sitemap regenerated** — 25 URLs, no duplicate privacy entry, priorities based on status (Active: 0.7, Occasional: 0.6, Archived: 0.5)
- **RSS regenerated** — 16 items with extracted descriptions, sorted by pubDate descending

### Shortcuts Panel — Final Design (stable, no further changes)
The panel was refactored from a modal dialog to a quiet reference card:
- **No backdrop** (`background: transparent`) — page remains fully visible; the card rests on it like a notebook page
- **Position** → `top: 4.5rem; left: calc(50% - 220px)` — anchored below nav, shifted left to belong to nav not page
- **Width** → 290px, compact and content-appropriate
- **Padding** → `1.25rem 1.5rem`
- **Border** → `1px solid rgba(37,34,32,0.6)` — soft but defined
- **Title** → `0.82rem`, `text-secondary`, weight 500
- **Section titles** → `0.6rem`, weight 500, uppercase, `opacity: 0.6`
- **List gap** → `0.35rem 1.5rem` — vertical breathing room
- **Keycaps** → `background: rgba(22,20,18,0.6); border-color: rgba(37,34,32,0.4)` — boxes recede, letters read first
- **Transition** → `0.08s`; `none` under `prefers-reduced-motion`
- **Label** → "Show shortcuts" (not "Reopen this card")
- **Alt note** → "Hold Alt (⌥) to reveal navigation shortcuts."
- **Responsive** → ≤ 700px: centered via `translate(-50%, -50%)`; ≤ 525px: 80% width

Guidelines for future changes:
- Treat the card as a mature component. Make it simpler, not richer.
- Verify keyboard accessibility: focus moves into card on open, Tab order predictable, Escape closes and returns focus to trigger element.
- Test at 125%, 150%, 200% zoom and on high-DPI displays.
- Ensure card never overlaps search dropdown or other overlays (every floating surface has a clear z-order).
- Keep shortcut list stable — users build muscle memory.
- Respect `prefers-reduced-motion`.
- Test entirely with keyboard: discover panel, navigate, close, continue reading.
- Gate every future change on: "Does this help someone return to reading more quickly?"

### In Progress
- **Mobile-first navigation redesign** – hamburger menu ≤ 520px, mobile menu panel, touch targets, responsive tables and typography
- **Pass 2: Home + Agents rendering** — rewrite prose, drop first person, update metadata

### Blocked
(none)

## Mobile Architecture
The mobile experience is designed as its own first-class interface, not a scaled-down desktop:
- **Navigation** collapses to a hamburger toggle at ≤ 520px with a simple, calm dropdown menu; search becomes icon-only at ≤ 650px
- **Touch targets** are ≥ 44px for all interactive elements (search btn, nav links, ranking list items, auth buttons)
- **Tables** have forced horizontal scroll on screens ≤ 720px to prevent overflow
- **Auth page** buttons go full-width on mobile for easy tapping
- **Typography** scales down at 600px (16px base) and 400px (tighter spacing); line length remains comfortable
- **Agent meta** grid collapses to single column at 768px
- **Shortcuts panel** re-centers on mobile (position: fixed, translate(-50%, -50%))
- **Search** at narrow widths uses `calc(100vw - 2rem)` to avoid overflow
- **Menu closes automatically** on Escape, outside click, and search focus – never overlaps with other overlays
- **Reduced motion** respected – hamburger animation and all transitions disabled
- Every page includes the same nav-toggle button for consistent mobile behavior

## Key Decisions
- Auth state stored in `localStorage` for persistence; `sessionStorage` for OAuth CSRF state and return URL
- GitHub OAuth token exchange delegated to Cloudflare Worker to keep `client_secret` server-side
- Client ID (`Ov23liMMYiMlgYzGg2Ht`) and worker URL are public; client secret is never in the repo
- Search index is pre-built via `build-index.py` (Python, stdlib only) to a static `search-index.json`
- Search changed from overlay modal to inline nav search (no page interruption)
- Nav restructured into three groups for explicit visual hierarchy
- Keyboard hints hidden by default because they are discover-through-use, not instructions
- Logo hover uses opacity-only to avoid competing with navigation links
- Search results show breadcrumb + snippet (no separate title line); repetitive "CLI Agents" suffix eliminated
- Auth return URL uses `sessionStorage` (survives redirect, auto-clears) instead of encoding in OAuth state or redirect_uri
- build-index.py scans filesystem for agent directories so adding a new agent automatically includes it in search after rebuild
- Footer "Shortcuts" label replaces `?` for immediate understandability
- Shortcuts panel has no backdrop — the page underneath is part of the experience
- Design direction shifted from "quieter" to "disappearing" — making the interface fade so the content leads

## Review Philosophy
- Reviews document understanding, not preference. A review should help the reader understand what a tool is, how it behaves in practice, where it succeeds, and where it falls short. The purpose is not to persuade readers toward or away from a tool, but to record careful observations grounded in evidence.
- Every significant claim should be traceable to sustained use, direct observation, or verifiable documentation. If a statement doesn't belong to one of those categories, it probably shouldn't be in the review.
- Current assessment answers "Where does this tool currently belong?" not "Should you use this?"

## Next Steps (Engineering, not UI)
1. **Rewrite Home page** — remove "my" language, align tone with About and Ethos
2. **Rewrite Methodology page** — replace "I evaluate" voice, align with new template philosophy
3. **Rewrite Agents index page** — reduce prominence of non-Active tools
4. **Server-render ranking list** in homepage HTML so content exists when JS is disabled
5. **Regenerate after content changes** — single command: `python3 build.py` (generates agents.js, search-index.json, rss.xml, sitemap.xml)
6. **Decide: which Archived tools remain vs removed entirely**
7. **Create Kilo page** only after sufficient use to support a thoughtful review
8. **Second consistency pass** — tone, headings, metadata, level-of-detail across all rewritten pages

## Critical Context
- Site is a pure static HTML/CSS/JS site on GitHub Pages; no build tool, no framework, no package manager
- 25 HTML pages across site; all share identical three-group nav structure
- `script.js` only included on 5 top-level pages; individual agent pages have no JS but include `search.js`
- Cloudflare Worker URL: `https://auth-worker.harpertoken-welcome.workers.dev`
- GitHub OAuth App client ID: `Ov23liMMYiMlgYzGg2Ht`
- Client secret: `5276d25c31fb2c428963c76e0fa0b358b8caeb24` (stored only in Cloudflare, never in repo)
- `auth.js` exposes `_config` and `_getStoredState`/`_clearStoredState` for callback page use
- `build.py` replaces old `build-index.py`; generates agents.js, search-index.json, rss.xml, sitemap.xml from a single command: `python3 build.py`
- All transitions now < 150ms; no scaling or movement on hover
- Search injects into `.nav-right` (not direct nav container)
- The interface is considered stable; future work should prioritize writing and engineering over design
- Shortcuts panel has no backdrop; it rests on the page like a reference card
- `data.js` is now the canonical org source (handwritten: id, status, order, addedDate); no longer loaded in browser
- `agents.js` is the generated runtime file (merged org + extracted HTML metadata); loaded by Home and Agents pages
- `build.py` extracts from agent HTML: name (h1), developer, version, lastUpdated — so updating a review requires editing one page and running `python3 build.py`
- CSS status indicators changed from old verdict classes to `.status-active`, `.status-occasional`, `.status-archived`
- `script.js` uses `a.status` for rendering; old `verdictClass()` and `a.verdict` references removed

## Relevant Files
- `auth.js` — Auth module with OAuth flow, CSRF state, return URL persistence, email stubs
- `auth/index.html` — Sign-in page with GitHub OAuth and email buttons
- `auth/callback/index.html` — OAuth callback handler with state validation, return URL redirect, redirect protection
- `workers/auth-worker.js` — Cloudflare Worker for code→token exchange (deployed)
- `wrangler.jsonc` — Worker deployment config (name: auth-worker, compatibility_date: 2026-06-30)
- `.gitignore` — Ignores `.wrangler/` alongside `.DS_Store`
- `build.py` — Python script to generate `agents.js`, `search-index.json`, `rss.xml`, `sitemap.xml` from canonical sources; scans agents/ directory dynamically; single command: `python3 build.py`
- `data.js` — Handwritten org data (id, status, order, addedDate); consumed only by `build.py`
- `agents.js` — Generated runtime file (merged org + extracted HTML metadata); loaded by Home and Agents pages
- `search-index.json` — Pre-built static search index
- `search.js` — Inline nav search; dropdown results with breadcrumb + snippet; keyboard nav (`↑`/`↓`/`Enter`/`Esc`/`/`); `/` keycap element; guards against hidden state
- `search/index.html` — Static fallback search page for JS-off access
- `script.js` — Keyboard shortcuts (H, A, M, B, E, S, /, ?, Esc); Alt/Option hint reveal; shortcuts panel; footer Shortcuts trigger; active page highlighting; status-based ranking and table rendering
- `styles.css` — Nav three-group layout; search dropdown at 420px with box-shadow; keycap styling; shortcuts panel (no backdrop, positioned below nav); responsive collapse rules; `.status-active/Occasional/Archived`
- `sitemap.xml` — Generated by build.py; 25 URLs, no duplicates, priorities by status
- `rss.xml` — Generated by build.py; 16 items with extracted descriptions
- `agent pages` (16 under `agents/`) — All rewritten using new template; each owns its own name, developer, version, dates in HTML
- `ethos/index.html` — H1 changed to "Ethos" (was "The Workshop") with updated intro prose
- `agents/index.html` — H1 and title changed to "Agents"; table now renders status column instead of verdict
