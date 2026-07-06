# Palmshed

Palmshed is a collection of careful observations on software, tools, and the practice of building. This site is published through an automated release pipeline.

The project values sustained use over first impressions, evidence over advocacy, and revision over certainty. Reviews describe what has been learned through continued use and are updated as understanding changes.

## Principles

The project is guided by five convictions:

- Patience
- Integrity
- Understanding
- Humility
- Stewardship

These are described in the Ethos page and are intended to become visible through the work itself.

## Reviews

Each review is written from sustained use where possible and clearly distinguishes observation from documented information.

Tools are grouped as:

- Active
- Occasional
- Archived

The grouping reflects the tool's current place within the project rather than a recommendation.

## Structure

```
/
├── about/
├── ethos/
├── methodology/
├── agents/
├── privacy/
├── search/
├── auth/
├── data.js
├── build.py
└── search-index.json
```

## Build

Generated artifacts are produced with:

```bash
python3 build.py
```

This regenerates the search index, RSS feed, sitemap, and other derived data.

## Contributing

Corrections, factual improvements, and well-supported suggestions are welcome.

## License

See the repository license.