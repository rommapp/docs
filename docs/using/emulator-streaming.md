---
title: Emulator Streaming
description: Launch games into a native emulator running in a container
---

# Emulator Streaming

Emulator streaming launches a game into a **native** emulator running in a separate container and streams the picture, sound, and input back to your browser. Unlike [in-browser play](in-browser-play/emulatorjs.md), the emulation runs server-side on real emulator binaries (PCSX2, Dolphin, RPCS3, RetroArch and friends), so the heavy lifting happens on the host rather than in the client. RomM claims a container, tells its broker which ROM to launch, and shows the live stream inside a player view with save, state, volume and disc controls.

Streaming runs on a [docker-webstation](https://github.com/linuxserver/docker-webstation) container: a [Selkies](https://github.com/selkies-project/selkies) WebRTC desktop with every supported emulator installed, plus the [romm-broker](https://github.com/romm-streaming/romm-broker) sidecar that RomM talks to. One container serves **every** platform you point at it. Nothing appears in the UI until you configure at least one.

A platform RomM can both emulate in the browser and stream offers the two as separate actions, so browser play stays available on a platform you also stream.

<!-- prettier-ignore -->
!!! info "Coming from the per-emulator broker mods?"
    A container without `protocol: webstation` still works, logs a startup warning, and will stop being supported in a future release. See [Migrating to webstation](emulator-streaming-migration.md) for the config rewrite.

## How a session works

A container drives one display, so it holds **one session at a time**, whatever platform that session is playing. Sessions live in [Valkey](../install/redis-or-valkey.md) behind an atomic claim, so several API workers stay consistent. A session is bound to the user who claimed it, and only that owner or an admin can control or release it.

Configure a platform on more than one container and those containers become a **pool**. A claim walks them in config order and takes the first free one, so two people can play the same platform at once as long as there is a container each. When every container is held, RomM looks for sessions whose heartbeat has gone stale (a closed tab, a crashed browser) and tears those down before reporting the platform busy.

Pool members have to agree on `emulator`, `memory_card_sync` and `protocol`. Those decide where saves are filed and which controls exist, so a player landing on either member has to find the same setup. Containers that disagree are treated as separate setups rather than a pool.

## Supported platforms

The broker ships standalone emulators for the platforms below, and RetroArch for everything else.

| Platform slug       | Emulator    | Save states                 | Memory card | Disc swap |
| ------------------- | ----------- | --------------------------- | ----------- | --------- |
| `ps2`               | PCSX2       | Slots 1-9, autosave slot 10 | Yes         | Manual    |
| `ngc`               | Dolphin     | Slots 1-7, autosave slot 8  | Yes         | -         |
| `wii`               | Dolphin     | Slots 1-7, autosave slot 8  | -           | -         |
| `psx`               | DuckStation | One resume state            | -           | -         |
| `ps3`               | RPCS3       | One resume state            | -           | -         |
| `xbox`              | xemu        | -                           | -           | -         |
| `xbox360`           | Xenia       | -                           | -           | -         |
| `wiiu`              | Cemu        | -                           | -           | -         |
| `switch`            | Eden        | -                           | -           | -         |
| `3ds`               | Azahar      | -                           | -           | -         |
| `ps4`               | shadPS4     | -                           | -           | -         |
| `psp`               | PPSSPP      | -                           | -           | -         |
| `dc`                | Flycast     | -                           | -           | Yes       |
| _(anything else)_   | RetroArch   | One resume state            | -           | Varies    |
| _(adventure games)_ | ScummVM     | One resume state            | -           | -         |

RetroArch serves dozens of platforms from one container and the broker picks the libretro core, so RomM labels the action with that core's name (`RA Snes9x`, `RA mGBA`). RomM never selects a core itself, that is the broker's `retroarch_platforms.json`.

The broker launches ROMs as direct files, so **archive extraction is not supported**.

## Saves and save states

Three different things travel between a container and your library, and which ones apply depends on the platform.

### Save states

**Save states** are the emulator's own snapshots. Platforms fall into three groups, per the table above:

- **Numbered slots plus an autosave slot** (PCSX2, Dolphin). The autosave slot is reserved for save-and-exit and is overwritten on the next exit.
- **One resume state** (DuckStation, RPCS3, RetroArch, ScummVM). These emulators write a state as they terminate, so there is no slot grid, just the single state that save and resume both land in.
- **No states at all** (xemu, Xenia, Cemu, Eden, Azahar, shadPS4). Persistence is the game's own save data instead.

Each state is copied off the container into your library as it is written, with a thumbnail grabbed from the stream canvas alongside it, and the state written by save-and-exit is filed when the session ends. Your stored states are pushed back down when you claim a container, so they roam across containers and survive a container rebuild. RomM keeps the newest states per game, emulator, and user, and prunes the rest past `STREAMING_STATE_HISTORY_LIMIT` (default `50`, `0` to keep everything).

These streaming states are stored separately from RomM's [per-user saves and states](saves-and-states.md) from in-browser play, since the file formats do not interchange.

### In-game saves

The emulator's **own** save data (NAND, battery saves, the emulated user profile) is pulled off the container as a single zip archive when a session ends, and stored as one save asset so the whole set travels as a unit. This is what persists progress on the platforms with no save states.

### Memory cards

On **PS2** and **GameCube**, you can opt a container into whole-card sync with `memory_card_sync: true`. The card then lives in your RomM library rather than on the container: RomM loads your card in when a session starts, copies it back when you exit, and leaves the container's slot blank in between. Whole-card sync **replaces** the in-game save path above for that container.

Cards are a library of their own. You can keep several, name and rename them, snapshot the current state as a version and roll back to one, share a card with other users, and download it. Your most recently used card for that emulator loads by default.

Setting `memory_card_sync` on a platform RomM knows has no card (Wii, xemu) is ignored with a warning, and individual save files sync instead. Honouring it there would shuttle an empty card around while the saves the platform actually uses stopped syncing.

PCSX2 only serves its card when Slot 1 holds a **Folder** card rather than a **File** card. With a File card the broker refuses the transfer and the session will not start, so set the card type before turning the flag on (see the [PCSX2 memory card setup](https://github.com/LoneAngelFayt/pcsx2-romm-integration#memory-card-setup)). Dolphin pins its own folder card, so GameCube needs no extra setup.

Because each session starts from your library, the first time RomM uses a container that already has a card on it, it stops and asks what to do:

- Importing it stores the container's card in your library, as a new version of your current card for that emulator, or as your first card if you have none.
- Starting fresh erases the container's card, which is confirmed first because it cannot be undone.

RomM records your answer per container, so it only asks once.

<!-- prettier-ignore -->
!!! warning "Playing on the container directly"
    Syncing only happens around a RomM streaming session. If you play on the emulator container directly, outside RomM, those saves and cards stay on the container and are not pulled into your library. A later RomM session loads your library's copy over them, so make your progress through RomM to keep it.

## Multi-disc games

A multi-disc game boots its playlist, and on `dc`, `saturn`, `segacd`, `turbografx-cd` and `dos` the mounted disc can be changed without restarting the emulator. Only the game's own playlist entries are valid swap targets.

Whichever disc was mounted when a state was written is the disc remounted when that state is loaded, so a save made on disc 3 resumes on disc 3.

PS2 has no swap route, but PCSX2's own UI can change discs from inside the stream.

## Joining a session

A session can be opened to a second player, and any user can see which sessions are joinable and ask to join one. Joining attaches to the running session rather than claiming a container, so it doesn't consume a second one.

## Administration

Two admin-only capabilities sit on top of the per-user session model:

- **Desktop sessions** open a container's desktop with no game running, which is how you configure an emulator inside the container that will run it (BIOS paths, controllers, per-emulator settings). A desktop claims the container under the same lock as a game, so it blocks players and a running game blocks it.
- **The container fleet** lists every configured container, what it is currently running and who claimed it, and can force-release any session. It is one row per container rather than per platform, because a container serving five platforms still holds one session. A container RomM cannot claim (a `host` with no scheme, no reachable broker) is listed as unconfigured rather than idle, so the misconfiguration is visible.

Force-releasing is also how you recover a platform stuck as in use when an owner disconnected without releasing it.

## Setup

### Run the webstation container

Stand up [docker-webstation](https://github.com/linuxserver/docker-webstation) with [romm-broker](https://github.com/romm-streaming/romm-broker), mounting your ROM library read-only. The container exposes two things RomM needs:

- The **Selkies web UI** the browser loads the stream from.
- The **broker API** RomM sends launch, save, state and disc commands to, served under the container's `SUBFOLDER` on the same origin.

A worked compose file lives in [`docker-compose.streaming.yml`](https://github.com/rommapp/romm/blob/master/docker-compose.streaming.yml) upstream. The image is amd64-only.

### Set up `config.yml`

Add a `streaming` block with **one entry per container**, full schema in [Configuration File → `streaming`](../reference/configuration-file.md#streaming). Container-level keys are the defaults for every platform it serves, and a platform block only names what differs.

```yaml
streaming:
    enabled: true
    containers:
        - protocol: webstation
          host: https://192.168.1.56:3010
          subfolder: /streaming
          library_path: /romm
          broker_secret: change-me
          label: Emulation station
          platforms:
              snes: retroarch # just the emulator name...
              ps2: # ...or a block overriding container keys
                  emulator: pcsx2
                  label: PCSX2
                  memory_card_sync: true
              ngc:
                  emulator: dolphin
                  label: Dolphin
                  memory_card_sync: true
```

- `host` is browser-facing and must be served over **HTTPS**, since Selkies WebRTC needs a secure context. Use the container's self-signed cert or a [reverse proxy with TLS](../install/reverse-proxy.md). A path (`/streaming`) works too when the container is reverse proxied onto RomM's own origin, in which case you have to name `broker_host` yourself, because a bare path carries no address RomM can dial.
- `subfolder` matches the container's `SUBFOLDER` and is what the broker routes hang off.
- `broker_host` is called server-side, so HTTP is fine. Omitted, a webstation container derives it from `host`. Pool members are identified by their broker host, so two containers pooling for a platform need distinct ones.
- `library_path` is where the container sees your ROM library, when that differs from RomM's own `/romm/library`. Keep it stable across a container rebuild so state and save history stays attached.
- `emulator` names the state and memory-card namespace. Set it explicitly, so renaming a `label` later doesn't orphan stored states and cards.

### Set the shared secret

`STREAMING_BROKER_SECRET` authenticates calls to the broker, and has to match the container's `BROKER_SECRET`. Set the **same value** on every container. If a broker needs a different secret, set `broker_secret` on that entry in `config.yml` and leave `STREAMING_BROKER_SECRET` unset, because the env var wins over the per-container value whenever it carries one.

### Tune the timeouts

All set as env vars (see [Environment Variables](../reference/environment-variables.md)):

| Variable                        | Default | What it bounds                                                                        |
| ------------------------------- | ------- | ------------------------------------------------------------------------------------- |
| `STREAMING_LAUNCH_TIMEOUT`      | `600`   | How long a launch may take, covering package and archive extraction before boot       |
| `STREAMING_SAVE_TIMEOUT`        | `45`    | How long a save-and-exit may take, raise it if a broker's `SAVE_WAIT` exceeds it      |
| `STREAMING_STATE_HISTORY_LIMIT` | `50`    | Save states kept per ROM, emulator and user before the oldest are pruned, `0` for all |

## Troubleshooting

- **No stream action on a platform**: `streaming.enabled` is false, no container is configured for that platform slug, or the config didn't reload. The streaming config is fetched when the app loads, so refresh after editing `config.yml`.
- **Stream never loads**: the browser can't reach `host`, or `host` is not HTTPS. Confirm the Selkies URL opens directly in a browser over `https://` from the client machine.
- **Launch or save returns an error**: the server can't reach `broker_host`, or the secret doesn't match. Check that `STREAMING_BROKER_SECRET` is identical on RomM and the container, and that `broker_host` resolves server-side.
- **Container listed as unconfigured in the fleet**: its `host` has no scheme, or nothing reachable was named as its broker. RomM can't claim it.
- **Platform stuck as in use**: an owner disconnected without releasing. Wait for the heartbeat to go stale, or force-release it from the fleet.
- **"The previous session is still saving"**: an exit is still pulling state off the container. It clears on its own, try again shortly.

## Related

- [Migrating to webstation](emulator-streaming-migration.md): moving off the per-emulator broker mods
- [Configuration File → `streaming`](../reference/configuration-file.md#streaming): every key the block accepts
- [Saves & States](saves-and-states.md): the in-browser player's separate save store
