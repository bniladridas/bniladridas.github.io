# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-09-10

### Added
- Two round theme balls at footer keep new gradient no-border and previous dark bordered themes. Choice stored in localStorage.
- Quiet gradient background with faint 80px grid, like og-image.png (1200x630).
- Portfolio as Python server: `pip install bniladridas-portfolio` and `portfolio serve`.
- Social meta tags: og:title, og:description (116 chars), og:image, twitter:card, twitter:image from og-image.png.

### Fixed
- Mobile responsiveness: no horizontal overflow, adaptive grids, larger tap targets, stacked CTA.
- Prevent overlap near objective and quickstart on mobile by breaking snippet into multiline and constraining pre.
- Make og:image fetchable by moving thumbnail to assets/thumbnail.png and adding width, height, and type.
- Remove inline margins, add gap-top class for Key features, Architecture, and Highlights.

### Changed
- Site is single source: Site/ is canonical, src/bniladridas_portfolio/static is populated at build via force-include.
- Verify-human updated for gradient theme, all 37 checks now pass.

## [0.1.0] - 2026-09-08

### Added
- Portfolio with Traction (UE5 simcade racer) and Palmshed Sandbox (TypeScript sandbox runtime).
- GitHub Pages via Actions, favicon from GitHub avatar, scroll cue and top progress, header GitHub gradient sweep.
- Human-feel verification and E2E theme switch.

### Fixed
- Mobile overlap near objective and quickstart.
- Em dashes removed, full stop appended to descriptions.

[Unreleased]: https://github.com/bniladridas/bniladridas.github.io/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/bniladridas/bniladridas.github.io/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bniladridas/bniladridas.github.io/releases/tag/v0.1.0
