---
title: Releasing
description: How RomM releases are cut, published, and documented. Maintainer reference.
---

# Releasing

Maintainer reference. If you're not cutting a release, you don't need this page. User-facing release info is in [Release Notes & Migration](../releases/index.md).

## Cadence

Releases ship when they're ready, not on a schedule:

- **Patch (`5.0.1`, `5.0.2`)**: bug fixes, cut as needed and typically 1–4 per month.
- **Minor (`5.1.0`, `5.2.0`)**: additive features, cut whenever a cohesive batch of features is stable.
- **Major (`6.0.0`)**: breaking changes, planned well in advance and announced on Discord and GitHub before the cut.

## Version numbering

[SemVer](https://semver.org/) for breaking-change semantics:

- **MAJOR**: backwards-incompatible schema change, env var rename, or API-contract break
- **MINOR**: new feature, backwards-compatible
- **PATCH**: bug fix only

Alembic migrations run on every startup and stay backwards-compatible within a major version.

## Pre-release checklist

### 1. Merge pending PRs

- All release-milestoned PRs merged into `master`
- CI green on `master`
- Linter green: `trunk check --all`
- Tests green: `uv run pytest`

### 2. Bump version numbers

- `pyproject.toml` → `version = "X.Y.Z"`
- `frontend/package.json` → `"version": "X.Y.Z"`
- Hardcoded version strings (`backend/__init__.py`, etc.). `rg '__version__'` or `rg '5\.0\.0'` to find them

### 3. Update `env.template` if needed

If the release adds, renames, or removes env vars, `env.template` is the canonical reference. Add/rename/remove lines with inline comments. Keep alphabetical order per section.

The docs site auto-generates [Environment Variables](../reference/environment-variables.md) from `env.template` on every release. Skip this step and the docs drift.

### 4. Update the changelog

`CHANGELOG.md` at repo root: add a new section.

```md
## 5.0.0 (2026-04-18)

### Breaking

- ...

### Added

- Feature foo (#1234)
- ...

### Fixed

- Bug bar (#1235)
```

Link to the PRs and issues. This feeds into the GitHub Release notes.

### 5. Tag and push

```sh
git checkout master
git pull
git tag -a 5.0.0 -m "Release 5.0.0"
git push origin 5.0.0
```

The tag triggers the Docker build workflow: `rommapp/romm:5.0.0` (full) and `rommapp/romm:5.0.0-slim` get built and published to Docker Hub plus GHCR.

### 6. Publish the GitHub Release

```sh
gh release create 5.0.0 \
  --title "RomM 5.0.0" \
  --notes-file release-notes.md \
  --latest
```

Notes come from the `CHANGELOG.md` entry. For major releases, add a migration-guide link at the top.

### 7. Move the `latest` and major tags

The Docker workflow handles `5.0.0` and `5.0.0-slim` automatically. For `:latest` and `:5` (only on non-prerelease, non-LTS-old-major):

```sh
docker pull rommapp/romm:5.0.0
docker tag rommapp/romm:5.0.0 rommapp/romm:latest
docker tag rommapp/romm:5.0.0 rommapp/romm:5
docker push rommapp/romm:latest
docker push rommapp/romm:5
```

Normally automated in the release workflow — manual fallback above.

## Announcements

- **Discord `#announcements`**: short summary with a link to the GitHub Release
- **Reddit** (r/selfhosted, etc.): optional, only for major versions
- **Docs site version switcher**: publish a new `mike`-managed version of the docs (next section)

## Docs versioning

Docs are versioned with [`mike`](https://github.com/jimporter/mike). After a release:

```sh
# in rommapp/docs repo
uv run mike deploy --push --update-aliases 5.0 latest
```

This publishes `/5.0/` on the docs site and moves the `latest` alias to `5.0`. Older versions stay at their historical URL (e.g. `/4.8/`). Full context in [Versioning](../releases/index.md#docs-versions).

## Post-release

### Patch quickly if needed

If a regression ships in a release: cherry-pick the fix into a `5.0.x` branch, bump to `5.0.1` in `pyproject.toml` and `package.json`, tag, release, and move `:latest` to the new patch.

### Triage Day-1 issues aggressively

Expect a spike in issues immediately after a release. Breakage reports need immediate attention while nice-to-haves can wait — sort by impact rather than by who shouted loudest.

## Security releases

For security fixes:

1. Don't disclose in the commit message — use "fix" generically
2. Cut the release
3. **After** the release is live, publish a GitHub Security Advisory with the CVE, timeline, and affected versions
4. Announce in Discord with a short summary and an "update now" recommendation

## Breaking-change protocol

For major versions:

1. **Announce early.** Open a tracking issue at least a month out. Post to Discord.
2. **Document the migration.** Write the upgrade guide _before_ the release, ready at cut time.
3. **Deprecate first when possible.** Ship a warning in a minor release before removing in a major.
4. **Migration scripts.** If the breaking change requires user action, ship a script in `scripts/migrate_<version>.py` or similar.

For migration-guide style, [Upgrading to 5.0](../releases/upgrading-to-5.0.md) is the reference template.
