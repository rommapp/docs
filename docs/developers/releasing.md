---
title: Releasing
description: How RomM releases are cut, published, and documented. Maintainer reference.
---

# Releasing

Maintainer reference. If you're not cutting a RomM release, you don't need this page. See [Release Notes & Migration](../releases/index.md) for user-facing release info.

## Release cadence

RomM releases on a loose cadence, not scheduled, driven by readiness:

- **Patch (`5.0.1`, `5.0.2`):** bug fixes. Cut as needed, typically 1-4 per month.
- **Minor (`5.1.0`, `5.2.0`):** additive features. Cut when a cohesive batch of features is stable.
- **Major (`6.0.0`):** breaking changes. Planned well in advance, announced in the Discord + on GitHub.

## Version numbering

[SemVer](https://semver.org/) for breaking-change semantics:

- **MAJOR:** backwards-incompatible schema change, env var rename, or API-contract break.
- **MINOR:** new feature, backwards-compatible.
- **PATCH:** bug fix only.

Alembic migrations run on every startup, and migrations are backwards-compatible within a major version.

## Pre-release checklist

### 1. Merge pending PRs

- All release-milestoned PRs merged into `master`.
- CI green on `master`.
- Linter green: `trunk check --all`.
- Tests green: `uv run pytest`.

### 2. Update version numbers

- `pyproject.toml` → `version = "X.Y.Z"`.
- `frontend/package.json` → `"version": "X.Y.Z"`.
- Any hardcoded version strings (`backend/__init__.py`, etc.). `rg '__version__'` or `rg '5\.0\.0'` to find them.

### 3. Update `env.template` if needed

If the release adds / renames / removes env vars, `env.template` is the canonical reference. Add/rename/remove lines with inline comments. Keep alphabetical order per section.

The docs site auto-generates [Environment Variables](../reference/environment-variables.md) from `env.template` on every release. Skip this step and the docs drift.

### 4. Update changelog

`CHANGELOG.md` at repo root (if present): add a new section for the new version:

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

Link to the PRs / issues. This feeds into the GitHub Release notes.

### 5. Tag and push

```sh
git checkout master
git pull
git tag -a 5.0.0 -m "Release 5.0.0"
git push origin 5.0.0
```

The tag triggers the Docker build workflow: `rommapp/romm:5.0.0` (full) and `rommapp/romm:5.0.0-slim` are built and published to Docker Hub + GHCR.

### 6. Publish the GitHub Release

From the GitHub UI or `gh` CLI:

```sh
gh release create 5.0.0 \
  --title "RomM 5.0.0" \
  --notes-file release-notes.md \
  --latest
```

Release notes come from the `CHANGELOG.md` entry. For major releases, add a migration-guide link to the top of the notes.

### 7. Move the `latest` and major tags

The Docker workflow handles `5.0.0` and `5.0.0-slim` automatically. For `:latest` and `:5`:

```sh
# only for non-prerelease, non-LTS-old-major
docker pull rommapp/romm:5.0.0
docker tag rommapp/romm:5.0.0 rommapp/romm:latest
docker tag rommapp/romm:5.0.0 rommapp/romm:5
docker push rommapp/romm:latest
docker push rommapp/romm:5
```

(Normally automated in the release workflow, manual fallback above.)

## Announcements

- **Discord `#announcements`:** post a short summary with a link to the GitHub Release.
- **Reddit** (r/selfhosted, etc.): optional, for major versions.
- **Docs site version switcher:** publish a new `mike`-managed version of the docs. See [Docs versioning](#docs-versioning).

## Docs versioning

RomM's docs are versioned with [`mike`](https://github.com/jimporter/mike). After a RomM release:

```sh
# in rommapp/docs repo
uv run mike deploy --push --update-aliases 5.0 latest
```

This publishes `/5.0/` on the docs site and moves the `latest` alias to `5.0`. Older versions stay at their historical URL (e.g. `/4.8/`).

See the [Versioning section](../releases/index.md#docs-versions) in Release Notes for the full context.

## Post-release

### Patch if needed

If a regression ships in the release:

1. Cherry-pick the fix into a `5.0.x` branch.
2. Bump to `5.0.1` in `pyproject.toml` + `package.json`.
3. Tag and release.
4. Move `:latest` to the new patch.

### Track issues

Post-release, expect a spike in issues. Triage Day-1 issues aggressively: breakage reports need immediate attention, and nice-to-haves can wait.

## Security releases

For security fixes:

1. Don't disclose in the commit message. Use "fix" generically.
2. Cut the release.
3. **After** the release is live, publish a GitHub Security Advisory with the CVE, timeline, and affected versions.
4. Announce in Discord with a short summary and an "update now" recommendation.

## Breaking-change protocol

For major versions:

1. **Announce early.** Open a tracking issue at least a month out. Post to Discord.
2. **Document the migration.** Write the upgrade guide _before_ the release, so it's ready at cut time.
3. **Deprecate first when possible.** Ship a warning in a minor release before removing in a major.
4. **Migration scripts.** If the breaking change requires user action, ship a script in `scripts/migrate_<version>.py` or similar.

## See also

- [Release Notes & Migration](../releases/index.md): user-facing side.
- [Upgrading to 5.0](../releases/upgrading-to-5.0.md): reference migration guide style.
- [Contributing](contributing.md): general contribution process.
