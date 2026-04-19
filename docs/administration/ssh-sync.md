---
title: SSH Sync
description: Configure SSH key-based push/pull sync to handhelds and other devices.
---

# SSH Sync

RomM's Push-Pull Device Sync task can push saves/states to registered devices and pull them back after a session, over SSH, using a key that RomM holds. This page covers the server-side setup.

The client side (a handheld running Grout, a SteamDeck running DeckRommSync, etc.) lives in [Integrations & Ecosystem](../ecosystem/index.md). The wire protocol (API-level sync negotiation, play-session ingest) lives in [Device Sync Protocol](../ecosystem/device-sync-protocol.md).

<!-- prettier-ignore -->
!!! note "Most companion apps don't need this"
    Argosy, Playnite, and most mobile/desktop clients sync via HTTPS + Client API Tokens. SSH sync is specifically for handhelds and similar devices where RomM pushes files to a filesystem the device exposes via SSH, with Grout on muOS / NextUI being the canonical case.

## When you need SSH sync

- A handheld running custom firmware exposing SSH (muOS, NextUI, Batocera, etc.).
- You want RomM to automatically copy saves/states to the device and pull them back when a session ends.
- Your sync runs on a schedule, not on-demand.

If none of that applies, you don't need this page. HTTPS + Client API Tokens is simpler and more flexible.

## Configuring the server

### 1. Provision an SSH key for RomM

Generate a dedicated key on the host that runs the RomM container:

```sh
ssh-keygen -t ed25519 -f ~/romm-sync-key -N "" -C "romm-sync"
```

This produces `~/romm-sync-key` (private) and `~/romm-sync-key.pub` (public). Keep the private key readable only by you: `chmod 600 ~/romm-sync-key`.

### 2. Mount the key into the RomM container

```yaml
services:
    romm:
        volumes:
            - /home/you/romm-sync-key:/romm/.ssh/id_rsa:ro
        environment:
            - SSH_PRIVATE_KEY_PATH=/romm/.ssh/id_rsa
```

Keep it read-only. RomM doesn't need to modify the key.

`SSH_PRIVATE_KEY_PATH` can point anywhere inside the container, conventionally `/romm/.ssh/id_rsa`.

### 3. Restart RomM

```sh
docker compose up -d
```

The Push-Pull Device Sync task will now use that key for outbound SSH connections.

## Configuring a device

For each handheld / device you want to sync:

### 1. Authorise the RomM key

Copy the **public** key (`~/romm-sync-key.pub` from step 1 above) to the device's `~/.ssh/authorized_keys`. Exactly how depends on the device: Grout on muOS has a helper, others expose a filesystem you can `ssh-copy-id` into.

### 2. Register the device in RomM

Device registration is done through a companion app (typically Grout itself) using the [Client API Token pairing flow](../ecosystem/client-api-tokens.md). Once registered, RomM knows:

- Device name + type.
- Hostname / IP.
- SSH port (default `22`).
- Target paths on the device for saves, states, and any other synced assets.

### 3. Test the connection

From the RomM container, confirm SSH works:

```sh
docker exec romm ssh -i "$SSH_PRIVATE_KEY_PATH" user@<device-ip> echo ok
```

You should see `ok`. If you see a host-key prompt, accept it. RomM will remember it in its `known_hosts`. If you see `permission denied`, the authorised key isn't installed correctly.

## How sync runs

The **Push-Pull Device Sync** scheduled task (default: every 15 minutes) does, for each registered device:

1. Connects via SSH.
2. Lists saves/states on the device and compares against RomM's DB.
3. Uploads (push) anything the device is missing.
4. Downloads (pull) anything newer on the device.
5. Updates play session records if the device reports any.

Tune the schedule via `PUSH_PULL_SYNC_INTERVAL_CRON`. See [Scheduled Tasks](scheduled-tasks.md).

Disable sync for a specific device by deregistering it from **Administration → Devices**, or disable the task entirely by unsetting / neutering `PUSH_PULL_SYNC_INTERVAL_CRON`.

## Troubleshooting

- **`Permission denied (publickey)`**: authorised key isn't set up on the device, or the private key inside the container can't be read (check the file permissions and bind-mount flags).
- **`Host key verification failed`**: the device's host key changed (after a reinstall, typically). Shell into the container and remove the offending line from `~/.ssh/known_hosts`.
- **Sync silently doesn't run**: check `GET /api/tasks/status` for the Push-Pull task's state. "failed" points you at the error, and "never ran" means the cron isn't firing (see [Scheduled Tasks](scheduled-tasks.md)).
- **Connection times out**: the device is offline or the network path is blocked. Confirm reachability from the RomM container: `docker exec romm ping <device-ip>`.

More at [Device Sync Troubleshooting](../troubleshooting/sync.md).

## Security notes

- The RomM sync key has read-write access to save paths on every registered device. Compromise = every device's saves gettable. Don't reuse this key for anything else.
- Rotate the key periodically: regenerate, update the volume mount, re-authorise on each device.
- Use a dedicated unprivileged user on the device (not root), with write access scoped only to the save directories.
