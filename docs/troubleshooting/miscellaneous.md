---
title: Miscellaneous Troubleshooting
description: Catch-all for issues that don't fit the other troubleshooting pages.
---

# Miscellaneous Troubleshooting

## `Could not get twitch auth token: check client_id and client_secret`

Your IGDB credentials are wrong or revoked. Full fix in [Authentication Troubleshooting → IGDB](authentication.md#error-could-not-get-twitch-auth-token-check-client_id-and-client_secret).

## Viewing RomM logs

Whatever your deployment, the first debugging step is looking at the logs.

### Docker Compose

```sh
docker logs -f romm          # live tail
docker logs --tail 200 romm  # last 200 lines
```

### Kubernetes

```sh
kubectl logs -n romm deploy/romm -f
kubectl logs -n romm deploy/romm --tail=200
```

### Unraid / Synology / TrueNAS

Logs are available from the GUI container view, or via SSH using the Docker commands above.

### What to grep for

Most lines start with `INFO`, `WARNING`, or `ERROR`. Common filters:

```sh
docker logs romm 2>&1 | grep ERROR
docker logs romm 2>&1 | grep -iE 'auth|oidc|oauth'
docker logs romm 2>&1 | grep -iE 'scan|metadata'
docker logs romm 2>&1 | grep -iE 'database|redis'
```

## Container works, UI is blank / spinner forever

Open devtools → Network tab → reload. You're looking for:

- **404 on `/assets/index-*.js`**: nginx inside the container is misrouting. Restart the container.
- **WebSocket connection failed** → reverse proxy isn't forwarding WebSockets. See [Authentication Troubleshooting → WebSockets](authentication.md#400-bad-request-on-the-websocket-endpoint).
- **CORS error** → `ROMM_BASE_URL` doesn't match the URL you're actually accessing. Set it correctly and restart.

## Covers and screenshots don't load

Static media is served from `/romm/resources` through nginx. If images 404:

1. **Mount is wrong**: `docker exec romm ls /romm/resources` should show cached files after at least one scan.
2. **Permissions**: same fix pattern as [Synology permissions](synology.md).
3. **Scan hasn't run yet**: covers are fetched during scan. Run one.

## RomM is slow

Most common causes, in order:

1. **Hashing large files on spinning disks.** Check **Skip hash calculation** or move the library to SSD.
2. **Metadata provider rate limiting during scans.** Reduce `SCAN_WORKERS` or split scans by platform.
3. **Container on underpowered hardware.** Check CPU/RAM headroom with `docker stats romm`. If RAM is pegged, raise container limits or disable `WATCHER_ENABLED`.

## Upgrade broke something

1. Roll back the image tag to the version you were on.
2. Restore your DB dump from [Backup & Restore](../install/backup-and-restore.md).
3. Open a bug report with: old version, new version, the exact error or behaviour, and `docker logs romm` from the failed startup.

For 4.x → 5.0 specifically, read [Upgrading to 5.0](../releases/upgrading-to-5.0.md). The migration guide covers every known breaking change.

## It's not listed here

- [Discord](https://discord.gg/romm) `#help`: active, friendly, fast
- [GitHub Issues](https://github.com/rommapp/romm/issues): for reproducible bugs
- Include your RomM version, deployment method, logs (secrets redacted), and exact repro steps.
