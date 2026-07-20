---
title: Emulator Streaming
description: Launch games into a native emulator running in a container
---

# Emulator Streaming

Emulator streaming launches a game into a **native** emulator running in a separate container and streams the picture, sound, and input back to your browser. Unlike [in-browser play](in-browser-play/emulatorjs.md), the emulation runs server-side on real emulator binaries (PCSX2, Dolphin, xemu, Eden), so the heavy lifting happens on the host rather than in the client. The server claims a session, tells the emulator which ROM to launch, and shows the live stream inside a player view, with save-state and volume controls in the toolbar.

Each emulator runs in its own [linuxserver](https://docs.linuxserver.io) container with a [Selkies](https://github.com/selkies-project/selkies) WebRTC stream and a small HTTP broker sidecar that RomM talks to. Nothing appears in the UI until you configure at least one container.

<!-- prettier-ignore -->
!!! warning "Work in progress"
    This is the first release of the streaming framework and ships with four emulators. More integrations (rpcs3 for PS3, and others) are planned as separate follow-ups.

## Supported emulators

Each emulator ships as a companion Docker mod repo with the broker sidecar and a worked `docker-compose.yml`.

| Platform slug        | Emulator | Save states | Manual slots | Autosave slot | Broker repo                                                                           |
| -------------------- | -------- | ----------- | ------------ | ------------- | ------------------------------------------------------------------------------------- |
| `ps2`                | PCSX2    | Yes         | 9            | Slot 10       | [pcsx2-romm-integration](https://github.com/LoneAngelFayt/pcsx2-romm-integration)     |
| `ngc`, `wii`, `wiiu` | Dolphin  | Yes         | 7            | Slot 8        | [dolphin-romm-integration](https://github.com/LoneAngelFayt/dolphin-romm-integration) |
| `xbox`               | xemu     | Yes         | 9            | Slot 10       | [xemu-romm-integration](https://github.com/LoneAngelFayt/xemu-romm-integration)       |

The broker launches ROMs as direct files, so **archive extraction is not supported**.

Only **one session per platform** can be active at a time, since there is a single emulator container behind it. Sessions are stored in [Valkey](../install/redis-or-valkey.md) with an atomic claim, so multiple workers stay consistent. The session is bound to the user who claimed it, and only that owner or an admin can control or release it, though an admin can force-release a stuck session.

## Save states

The autosave slot is reserved for **Save & Exit**, so it can be overwritten on the next exit. Save files and states here live inside the emulator container and are **not** the same as RomM's [per-user saves and states](saves-and-states.md) from in-browser play.

## Setup

### Run the emulator containers

Pick the broker repos for the platforms you want and follow each repo's `docker-compose.yml`. Each container exposes two things we need:

- The **Selkies web UI** the browser loads the stream from (an HTTPS port).
- The **broker API** RomM sends launch, save, and volume commands to (default port `8000`).

### Setup `config.yml`

Add a `streaming` block with one entry per emulator container, full schema in [Configuration File → `streaming`](../reference/configuration-file.md#streaming).

- `host` must be reachable from clients and served over **HTTPS** (Selkies WebRTC requires a secure context). Use the container's built-in self-signed cert or a [reverse proxy with TLS](../install/reverse-proxy.md).
- `broker_host` is called server-side, so HTTP is fine. If the containers share a Docker network, use the container name (e.g. `http://pcsx2:8000`). If `broker_host` is omitted, it gets derived from `host`.
- `label` is the text shown on the play action.

Multiple platforms can share one container (point `ngc`, `wii`, and `wiiu` at the same Dolphin instance) or each use their own.

### Set the shared secret

`STREAMING_BROKER_SECRET` authenticates calls to the broker. Set the **same value** in every container. If a broker slot needs a different secret, a per-container `broker_secret` in `config.yml` overrides the env var for that entry.

If a broker's save wait exceeds the default 45 seconds, raise `STREAMING_SAVE_TIMEOUT` (seconds) so Save & Exit doesn't time out. Both are set as env vars (see [Environment Variables](../reference/environment-variables.md)).

## Troubleshooting

- **No Play on `<label>` action**: `streaming.enabled` is false, no container is configured for that platform slug, or the config didn't reload. The streaming config is fetched when the app loads, so refresh after editing `config.yml`.
- **Stream never loads**: the browser can't reach `host`, or `host` is not HTTPS. Confirm the Selkies URL opens directly in a browser over `https://` from the client machine.
- **Launch or save returns an error**: the server can't reach `broker_host`, or the secret doesn't match. Check that `STREAMING_BROKER_SECRET` is identical on both containers and that `broker_host` resolves server-side.
- **Platform stuck as "in use"**: an owner disconnected without releasing. The owner or an admin can force-release the session.
