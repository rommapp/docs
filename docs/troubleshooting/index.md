---
title: Troubleshooting
description: Diagnose common issues by symptom
---

# Troubleshooting

## RomM won't start

- Container crashes immediately → check `docker logs romm`. If it's `invalid host in "tcp://..."` you're on Kubernetes, see [Kubernetes Troubleshooting](kubernetes.md).
- Database connection errors → verify `DB_HOST`/`DB_PASSWD` match your DB container, and that the DB has finished initialising (first run takes longer than you'd think).
- "Page not found" on first load → wait, because initial migrations and resource seeding take a minute.

## No Setup Wizard

- If you do not see the setup wizard upon first connecting, and instead see a login screen, first check to see if the version number in the bottom right is `0.0.0`. If it is, RomM is functional and accessible, but not configured correctly,
  and you will not be able to login, no matter what username and password you try.
- Ensure that you have modified `path/to/library`,`path/to/assets`, and `path/to/configs` in your `docker-compose.yml` so that they point to directories on the host.
- `/romm/library`, `/romm/assets`, and `/romm/config` should remain unchanged, as these refer to directories inside the docker container itself.

## Login issues

- Getting 403s → [Authentication Troubleshooting](authentication.md)
- OIDC redirect fails → [Authentication Troubleshooting → OIDC](authentication.md#oidc)
- Forgot the admin password → reset via DB or a fresh admin invite from another admin account.

## Scanning problems

- Scan ends immediately, no platforms found → [Scanning Troubleshooting](scanning.md)
- Platform not detected → check folder slug matches [Supported Platforms](../platforms/supported-platforms.md) or add a `system.platforms` binding in [`config.yml`](../reference/configuration-file.md).
- Scan times out → [Scanning Troubleshooting](scanning.md)

## In-browser play

- EmulatorJS won't load/404 → [In-Browser Play Troubleshooting](in-browser-play.md) (on the slim image, cores come from a CDN at runtime, so a 404 usually means outbound networks are blocked).
- Netplay doesn't connect → [Netplay Troubleshooting](netplay.md), almost always NAT or missing ICE servers

## Platform-specific

- [Synology Troubleshooting](synology.md): permission errors, DSM gotchas
- [Kubernetes Troubleshooting](kubernetes.md): the `enableServiceLinks` fix and related

## Still stuck?

- [GitHub issues](https://github.com/rommapp/romm/issues): search first, then open if you've got a reproducible bug.
- [Discord](https://discord.gg/romm): `#help` channel, staffed by community + maintainers
