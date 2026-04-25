---
title: Device Sync Troubleshooting
description: Diagnose push-pull sync, Client API Token pairing, and companion-app connectivity.
---

# Device Sync Troubleshooting

Device Sync covers two distinct things:

- **API sync** (HTTPS, token-auth): used by most companion apps. Argosy, Playnite, RommBrowser, mobile apps
- **SSH sync** (push-pull task): used by handhelds. Grout on muOS, DeckRommSync on Deck, etc.

Troubleshooting paths differ.

## API-based sync (companion apps)

### App says "token invalid"

- **Token revoked.** Check Profile → Client API Tokens. Was it deleted?
- **Token expired.** Tokens can have optional expiry. Check the expiry date on the token page.
- **Scopes mismatch.** App needs scopes the token doesn't carry. Create a new token with the required scopes. See [Users & Roles → scope matrix](../administration/users-and-roles.md#scope-matrix).
- **User downgraded.** If the owning user got demoted (Admin to Viewer, say), tokens with scopes outside the new role stop working.

### App can't reach RomM

- **URL wrong.** Double-check what you entered in the app config. `https://demo.romm.app`, not `https://demo.romm.app/api` (the app appends the API path)
- **TLS cert issues.** Self-signed certs cause problems. Use a proper cert (Let's Encrypt through your reverse proxy) or configure the app to skip cert validation (not recommended).
- **Firewall.** From the device, `curl https://demo.romm.app/api/heartbeat`. Should return JSON. If not, network path is blocked.

### Pairing code doesn't work

The pairing flow: RomM generates a short code, device exchanges it for a full token.

- **Code expired.** Codes are short-lived (5 minutes default). Generate a new one.
- **Code already used.** Single-use. Generate a new one.
- **Device can't reach RomM.** Pairing still requires network access from the device to RomM's API.
- **User out of token slots.** 25-token max per user. Revoke an unused token first.

Full flow: [Client API Tokens](../ecosystem/client-api-tokens.md).

### Saves aren't appearing after playing on the device

- **Sync hasn't run yet.** The Push-Pull Device Sync task runs every 15 minutes by default. Check Administration → Tasks for last-run timestamp.
- **App didn't upload.** Open the app's logs. Some apps upload on app-close rather than on every save.
- **Wrong save location on device.** RomM reads from a specific path. If the app stored saves elsewhere, they won't sync. Check the device's save path configuration.

## SSH-based sync (handhelds)

### Permission denied (publickey)

RomM's SSH key isn't authorised on the device.

1. Verify the **public** key (from `~/romm-sync-key.pub` on the host) is in the device's `~/.ssh/authorized_keys`.
2. Check line breaks (CRLF vs LF issues bite here). The `authorized_keys` file should have one key per line, Unix line endings.
3. Check file permissions on the device: `~/.ssh/` should be `700`, `~/.ssh/authorized_keys` should be `600`.

See [SSH Sync → Configuring a device](../ecosystem/ssh-sync.md#configuring-a-device).

### Host key verification failed

The device's SSH host key changed (usually after a reinstall / reflash).

Fix from inside the RomM container:

```sh
docker exec romm ssh-keygen -R <device-ip>
```

Next sync cycle will accept the new host key.

### Can't read SSH key in container

```text
Permissions 0644 for '/romm/.ssh/id_rsa' are too open
```

OpenSSH refuses to use keys with loose permissions. On the host:

```sh
chmod 600 /path/to/romm-sync-key
```

And verify the Docker bind mount isn't forcing different perms (ro is fine but mode-reset-via-mount-option is the usual culprit).

### Sync task doesn't run

- **`SSH_PRIVATE_KEY_PATH` not set.** Check the RomM container's env. If the path doesn't exist inside the container, sync quietly no-ops.
- **No devices registered.** Administration → Devices. If empty, there's nothing to sync.
- **Cron expression wrong.** Default `PUSH_PULL_SYNC_INTERVAL_CRON=*/15 * * * *`. Invalid cron silently doesn't run.
- **Task failing silently.** `GET /api/tasks/status`: status shows per-task state. "failed" with a last-error is a direct pointer.

## Play sessions

Play sessions from a companion app (time-played tracking, Continue Playing ribbon):

- **Not appearing in RomM**: app isn't POSTing to `/api/play-sessions`. Check app's logs.
- **Duplicate sessions**: app is re-posting on sync. Known edge case for some companion apps, usually harmless
- **Times look wrong**: timezone mismatch between device and RomM. RomM stores UTC, and display converts to user TZ.

## Devices panel says "offline"

RomM sees no heartbeat from the device. Either:

- Device is genuinely off.
- Device's companion app has stopped phoning home. Check the app's logs / relaunch it.
- RomM last-seen threshold elapsed. Devices show online for 1 hour after last heartbeat. After that, offline

## Smart collection / filter isn't updating after sync

Smart collections re-evaluate on ROM / metadata change. A pure save upload doesn't trigger re-eval. If you have a Smart Collection tied to playtime, it updates on the next play session ingest.

Admins can force a re-eval via Administration → Tasks → Refresh Smart Collections.

## Still stuck

- **API sync**: `docker logs romm | grep -iE 'sync|device|token'`
- **SSH sync**: `docker logs romm | grep -iE 'push_pull|ssh'`
- Device-side logs from the companion app. Each app differs.
- [Discord](https://discord.gg/romm) `#help`: include the app name, its version, and the RomM log lines.

## See also

- [Client API Tokens](../ecosystem/client-api-tokens.md): token + pairing flow reference
- [Device Sync Protocol](../ecosystem/device-sync-protocol.md): wire-level protocol details
- [SSH Sync](../ecosystem/ssh-sync.md): server-side SSH sync config
- [Companion apps](../ecosystem/community-apps.md): list of integrations and their status
