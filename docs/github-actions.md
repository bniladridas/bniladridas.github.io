# GitHub Actions

## Workflows

### `build.yml`

**Purpose.** CI and GitHub Pages deployment in one workflow.

**Triggers.** Push to `main`; pull request targeting `main`.

**Behaviour.**

- Runs `python3 build.py` to regenerate all derived artifacts (`agents.js`, `search-index.json`, `rss.xml`, `sitemap.xml`).
- Fails if the generated files differ from what is committed — this keeps the repository consistent without manual rebuilds.
- On push to `main`: uploads the repository root as a Pages artifact and deploys to GitHub Pages.
- On pull requests: build and verify only. Pages steps are skipped.

---

### `release-pr.yml`

**Purpose.** Prepare a release by creating a pull request with freshly built artifacts.

**Trigger.** Manual (`workflow_dispatch`).

**Behaviour.**

- Checks out `main`, runs `python3 build.py`.
- If generated files have changed, commits them to the `release/prepare` branch and opens (or updates) a pull request back into `main` with the `release` label.
- If nothing has changed, exits cleanly without creating a PR.

Use this when you are ready to cut a release. Review the changes in the resulting PR and merge it to trigger the release workflow.

---

### `release.yml`

**Purpose.** Publish a GitHub Release when a release PR is merged.

**Trigger.** A pull request is merged into `main` and carries the `release` label.

**Behaviour.**

- Determines the next version number:
  - If a `VERSION` file exists, reads and validates it.
  - Otherwise, infers the next patch version from the latest tag (e.g. `v0.1.0` → `0.1.1`).
- Creates an annotated Git tag and pushes it.
- Creates a GitHub Release with auto-generated release notes.

Pages deployment is handled by `build.yml` — this workflow does not deploy.

---

## Release flow

1. Run the `release-pr` workflow (manual dispatch).
2. Review the resulting pull request.
3. Merge the pull request (ensure the `release` label is present).
4. The `release` workflow creates a tagged Release automatically.

## Verification checklist

### GitHub App permissions (`palmshed-steward`)

| Permission | Setting |
|---|---|
| Contents | **Read & Write** |
| Pull requests | **Read & Write** |
| Metadata | **Read** |
| Actions | **Read** if needed |

Administration is not needed. Restrict installation to only the Palmshed repository. The private key lives exclusively in `PALMSHED_APP_PRIVATE_KEY` — never in files or logs.

### Repository settings

| Setting | Value |
|---|---|
| Pages / Source | **GitHub Actions** |
| Actions / General / Workflow permissions | **Read and write permissions** |

The Pages setting lets `actions/upload-pages-artifact` and `actions/deploy-pages` serve the site. Workflow permissions are only needed as a fallback — the release workflows use `permissions: {}` and authenticate through the GitHub App token instead.

### Release flow (end-to-end)

```
Develop on main
       ↓
Run "release-pr" workflow (manual dispatch)
       ↓
Review / approve the resulting PR
       ↓
Merge (PR must carry the `release` label)
       ↓
release.yml
  • palmshed-steward[bot] creates annotated tag
  • palmshed-steward[bot] creates GitHub Release
       ↓
build.yml (triggered by the push to main)
  • builds and verifies generated files
  • deploys to GitHub Pages
```

Every published release goes through a reviewed PR before it is tagged and deployed. The release workflow is idempotent — re-running it when the tag or release already exists exits cleanly instead of failing.
