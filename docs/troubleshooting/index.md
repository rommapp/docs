---
title: Troubleshooting
description: Diagnose common issues by symptom
---

# Troubleshooting

If something's broken, start with the symptom that best matches:

## By symptom

### RomM won't start

- Container crashes immediately → check `docker logs romm`. If it's `invalid host in "tcp://..."` you're on Kubernetes, see [Kubernetes Troubleshooting](kubernetes.md).
- Database connection errors → verify `DB_HOST`/`DB_PASSWD` match your DB container, and that the DB has finished initialising (first run takes longer than you'd think).
- "Page not found" on first load → wait, because initial migrations and resource seeding take a minute.

### Login issues

- Getting 403s → [Authentication Troubleshooting](authentication.md)
- OIDC redirect fails → [Authentication Troubleshooting → OIDC](authentication.md#oidc)
- Forgot the admin password → reset via DB or a fresh admin invite from another admin account.

### Scanning problems

- Scan ends immediately, no platforms found → [Scanning Troubleshooting](scanning.md)
- Platform not detected → check folder slug matches [Supported Platforms](../platforms/supported-platforms.md) or add a `system.platforms` binding in [`config.yml`](../reference/configuration-file.md).
- Scan times out → [Scanning Troubleshooting](scanning.md)

### In-browser play

- EmulatorJS won't load/404 → [In-Browser Play Troubleshooting](in-browser-play.md) (on the slim image, cores come from a CDN at runtime, so a 404 usually means outbound networks are blocked).
- Netplay doesn't connect → [Netplay Troubleshooting](netplay.md), almost always NAT or missing ICE servers

### Platform-specific

- [Synology Troubleshooting](synology.md): permission errors, DSM gotchas
- [Kubernetes Troubleshooting](kubernetes.md): the `enableServiceLinks` fix and related

## Still stuck?

- [GitHub issues](https://github.com/rommapp/romm/issues): search first, then open if you've got a reproducible bug.
- [Discord](https://discord.gg/romm): `#help` channel, staffed by community + maintainers
