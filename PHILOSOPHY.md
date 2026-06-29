# Design Philosophy

This document explains the principles that guide every decision in this project. When making changes, follow these guidelines unless there is a strong engineering reason not to.

## Principles

**Simplicity over decoration.** Every element should earn its place. If removing it does not reduce understanding, remove it.

**Evidence over marketing.** Claims should come from experience, not from feature lists. Write what happened, not what the tool promises.

**Writing over visuals.** Typography is the primary design element. Visual hierarchy should serve readability, not decoration.

**Accessibility over trends.** Semantic HTML, keyboard navigation, and color contrast are non-negotiable. Design for everyone.

**Long-term maintainability over short-term appeal.** This site should still feel sincere in ten years. Avoid trends that will look dated.

**Respect the reader's time.** Be concise. Every sentence should either share an observation, explain a decision, or describe an experience.

**Build with restraint.** If a design decision exists only to attract attention, question whether it belongs. If it helps someone understand or navigate more easily, it probably belongs.

## Writing

Write as though leaving careful notes for another engineer. Do not try to convince, entertain, or sound like an expert.

- Use plain, natural English.
- Prefer short and medium sentences.
- Avoid hype words: revolutionary, game-changing, best-ever, next-generation, AI-powered.
- Avoid common AI writing patterns: "delve," "leverage," "unlock," "in today's rapidly evolving landscape."
- Avoid em dashes. End one sentence and begin another instead.
- Avoid emojis.
- Keep the tone calm, professional, and evidence-driven.
- Readers should leave feeling they learned something, not that they were marketed to.

## Design for Longevity

This website is built with a lifespan measured in years, not months. Do not follow trends simply because they are popular.

Choose patterns that have remained useful for decades. Prefer HTML over JavaScript where possible. Prefer typography over decoration. Prefer documentation over presentation.

### Avoid

These patterns tend to feel dated quickly and should be avoided:

- Oversized hero sections
- Glassmorphism or excessive blur
- Animated gradients
- Floating cards
- Endless scrolling effects
- Unnecessary page transitions
- Large loading animations
- Flashy or oversized hover effects
- Any decoration that exists only to impress

Use motion only when it improves understanding. Respect `prefers-reduced-motion`.

### Navigation

Users should always know where they are, where they came from, and where they can go next. Every page should be reachable within a few clicks.

### Reading Experience

Optimize for people who spend twenty minutes reading. Use comfortable line lengths (around 760px). Use generous spacing. Make headings meaningful. Allow readers to scan naturally.

### Performance

Pages should feel instant. Avoid unnecessary dependencies. Keep assets lightweight. Optimize for long-term maintainability rather than short-term novelty.

## Design

- No frameworks. Pure HTML, CSS, and JavaScript only.
- No analytics, advertisements, or tracking.
- No gradients, shadows, or decorative flourishes.
- No animations beyond subtle hover effects using CSS transform and opacity.
- Support dark mode and light mode via `prefers-color-scheme`.
- Mobile-first responsive design.
- Maximum content width around 760px for comfortable reading.
- Generous whitespace. Let the content breathe.

## Content

- Every agent review follows the same structure.
- Reviews are based on actual use, not feature comparisons.
- Rankings are subjective and will change as tools evolve.
- Update pages when opinions change. Do not defend old conclusions.
- Critique software respectfully. Never attack the people who built it.

## Code

- Semantic HTML. No div soup.
- Minimal JavaScript. Only what is necessary for functionality.
- No build step. The site is served as static files.
- Adding a new agent requires: one new directory, one review file, one entry in `data.js`. No redesign.
- Design components that can evolve without redesigning the site.

## Hierarchy

1. Content
2. Typography
3. Navigation
4. Branding

The logo indicates authorship. It should never compete with the content.

## Evolution

Design components that can evolve without redesigning the site. A new section, a new review, or a new article should fit naturally into the existing structure. Avoid layouts that require rebuilding the homepage every year.

Do not build a personal brand. Build a body of work. The website should become more valuable as more thoughtful writing is added.

A visitor should remember the quality of the ideas, not the appearance of the interface. If someone discovers this website many years from now, it should still feel calm, readable, and trustworthy.

Before merging any UX change, ask: "Will this still feel appropriate five years from now?"
