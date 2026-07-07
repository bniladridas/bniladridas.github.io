# AGENTS.md

## Purpose

This repository publishes careful reviews of software tools and related engineering work.

The goal is not to recommend products or build rankings. The goal is to document understanding that has been earned through sustained use and careful observation.

## Principles

Every contribution should reflect the project's ethos.

- Patience
- Integrity
- Understanding
- Humility
- Stewardship

These principles are expressed through the work rather than repeated in the writing.

## Writing

Use a quiet, direct style.

Avoid:

- marketing language
- hype
- exaggerated claims
- persuasion
- unnecessary adjectives
- first-person narrative unless historically necessary

Write concise paragraphs instead of long lists where possible.

## Reviews

Each review should follow the same structure.

1. Overview
2. Review context
3. Strengths
4. Limitations
5. Where it fits
6. Current assessment
7. Reference
8. Revision history

Every significant claim should be supported by one of:

- sustained use
- direct observation
- official documentation

State the basis of assessment whenever it is helpful to the reader.

## Status

Every reviewed tool belongs to one of three groups.

- Active
- Occasional
- Archived

Status describes the tool's current place within the project. It is not a recommendation.

## References

Verify every factual field before publishing.

Check:

- official website
- canonical repository
- maintainer or organization
- license
- supported platforms
- pricing
- version reviewed

Do not copy values between projects.

## Metadata

Structured metadata belongs in `registry/agents.js`.

Review prose belongs in the individual review page.

Generated files are produced by `scripts/build.py` and should not be edited directly.

## Source of truth

Handwritten:
- `registry/agents.js` — canonical editorial registry (id, status, order, addedDate)
- All HTML pages — review prose, about, ethos, methodology, privacy, auth

Generated (never edit directly):
- `agents.js`          — merged runtime data for the browser
- `search-index.json`  — full-text search index
- `rss.xml`            — RSS 2.0 feed
- `sitemap.xml`        — XML sitemap

Data flow:

```
registry/agents.js
        │
        ▼
scripts/build.py
        │
        ├── agents.js
        ├── search-index.json
        ├── rss.xml
        └── sitemap.xml
                │
                ▼
           Browser / Search / RSS
```

## Revisions

Reviews are expected to change as understanding develops.

When an assessment changes:

1. Update the review.
2. Update the review context if needed.
3. Update `registry/agents.js`.
4. Run `python3 scripts/build.py`.

Visible revisions are part of the project's commitment to truthful work.