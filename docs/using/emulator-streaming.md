---
title: Emulator Streaming
description: Launch games into a native emulator running in a container
---

# Emulator Streaming

Emulator streaming runs your game in a **real** emulator on the server and streams the video, audio and input to your browser. Where [in-browser play](in-browser-play/emulatorjs.md) compiles emulators to WebAssembly and runs them on your machine, this runs actual PCSX2, Dolphin, RPCS3 and RetroArch binaries on the host. Your browser is just a screen.

It all runs in one [docker-webstation](https://github.com/linuxserver/docker-webstation) container: a [Selkies](https://github.com/selkies-project/selkies) WebRTC desktop with the emulators installed, plus the [romm-broker](https://github.com/romm-streaming/romm-broker) sidecar RomM sends commands to. A single container handles **every** platform you point at it. Until you configure one, none of this shows up in the UI.

If a platform can do both, you get separate actions for browser play and streaming, so turning on streaming doesn't take browser play away.

<!-- prettier-ignore -->
!!! info "Coming from the per-emulator broker mods?"
    A container without `protocol: webstation` still works, but will stop being supported in a future release. See [Migrating to webstation](emulator-streaming-migration.md) for the config rewrite.

## How a session works

There's one display per container, so a container runs **one session at a time** no matter which platform it's playing. Sessions are stored in [Valkey](../install/redis-or-valkey.md) and claimed atomically, which keeps multiple API workers from stepping on each other. Whoever claims a session owns it, and only they or an admin can control or release it.

List the same platform on several containers and you get a **pool**. RomM walks them in config order and grabs the first free one, so two people can play SNES at once if you've got two containers. If they're all busy, RomM checks for sessions whose heartbeat has gone quiet (someone closed a tab, a browser crashed) and clears those out before telling you the platform is in use.

Containers only pool together if they agree on `emulator`, `memory_card_sync` and `protocol`. Those three decide where saves end up and which controls the player offers, and it would be a bad surprise to land on a pool member and find your saves missing. Containers that differ are treated as separate setups.

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

RetroArch covers dozens of platforms from the one container. The broker picks the core, not RomM, and RomM just labels the action with whatever core that is (`RA Snes9x`, `RA mGBA`). If you want to change the mapping it's the broker's `retroarch_platforms.json`.

ROMs are launched as plain files, so **archives won't work**. Extract them first.

## Saves and save states

Three separate things move between the container and your library. Which ones apply depends on the platform.

### Save states

These are the emulator's own snapshots, and the table above says which of three shapes each platform gets:

- **Numbered slots with an autosave.** The autosave slot belongs to save-and-exit and is overwritten every time you exit, so don't keep anything there.
- **A single resume state.** These emulators only write a state as they shut down, so there's no grid to pick from, just the one state that saving and resuming both use.
- **No states at all.** You rely on the game's own save data instead.

Whenever a state is written, RomM copies it off the container, along with a thumbnail grabbed from the video. The state from save-and-exit is collected when the session closes. Claim a container later and RomM pushes your stored states back onto it, which is why they follow you between containers and survive a container being rebuilt.

RomM keeps the most recent `STREAMING_STATE_HISTORY_LIMIT` states per game, per emulator, per user (default `50`, or `0` to keep everything) and prunes the rest.

These are kept apart from the [saves and states](saves-and-states.md) that in-browser play produces, because the formats aren't interchangeable.

### In-game saves

This is the save data the game itself writes: NAND, battery saves, the emulated user profile. When a session ends, RomM zips the lot off the container and stores it as a single save, so it all stays together. On platforms with no save states, this is the only thing keeping your progress.

### Memory cards

On **PS2** and **GameCube** you can set `memory_card_sync: true` and have RomM manage the whole card instead of individual save files. The card lives in your library: RomM loads it in when a session starts, copies it back when you exit, and leaves the container's slot empty in between. This **replaces** the in-game save handling above for that container.

Cards are their own little library. Keep as many as you like, name and rename them, snapshot the current state as a version and roll back to it later, share one with another user, or download it. Whichever card you used last loads by default.

Set the flag on a platform with no memory card (Wii, xemu) and RomM logs a warning and ignores it, syncing individual save files instead. Obeying it would mean shuffling an empty card back and forth while the saves those platforms actually use stopped syncing.

PCSX2 needs Slot 1 set to a **Folder** card, not a **File** card. Given a File card, the broker refuses to hand it over and the session won't start at all. Change the card type before you turn the flag on (see the [PCSX2 memory card setup](https://github.com/LoneAngelFayt/pcsx2-romm-integration#memory-card-setup)). Dolphin pins its own folder card, and GameCube works out of the box.

Every session starts from your library's copy, so the first time RomM meets a container that already has a card sitting on it, it stops and asks:

- **Import it**, and the container's card goes into your library, either as a new version of your current card or as your first one.
- **Start fresh**, and the container's card is wiped. You get a confirmation first, since there's no undo.

RomM remembers your answer per container and won't ask again.

<!-- prettier-ignore -->
!!! warning "Playing on the container directly"
    Syncing only happens at the start and end of a RomM session. Play on the container directly, outside RomM, and those saves and cards never reach your library. Worse, the next RomM session will write your library's copy over them. Go through RomM if you want to keep the progress.

## Multi-disc games

Multi-disc games boot their full playlist. On `dc`, `saturn`, `segacd`, `turbografx-cd` and `dos` you can change discs without restarting the emulator, choosing from that game's own discs.

RomM records which disc was mounted when you saved a state and remounts the same one when you load it, so a save on disc 3 comes back on disc 3.

PS2 has no swap control, but you can change discs from inside PCSX2 itself.

## Joining a session

You can open a session up to a second player. Anyone can see which sessions are joinable and ask to join. Joining hooks into the running session rather than claiming a container of its own, so it doesn't eat a second one.

## Administration

Admins get two extra things:

**Desktop sessions** give you the container's desktop with no game running. This is how you set an emulator up from the inside: BIOS paths, controllers, whatever per-emulator settings it needs. A desktop takes the same lock a game does, so it blocks players out and a running game blocks you out.

**The container fleet** shows every container you've configured, what it's running and who claimed it, and lets you force-release any session. Rows are per container, not per platform, since a container serving five platforms still only holds one session. Anything RomM can't claim (a `host` missing its scheme, a broker it can't reach) shows as unconfigured rather than idle, so a typo is visible instead of silent.

Force-release is also your way out when a platform is stuck as in-use because someone closed their browser without releasing it.

## Setup

### Run the webstation container

Start [docker-webstation](https://github.com/linuxserver/docker-webstation) with [romm-broker](https://github.com/romm-streaming/romm-broker), mounting your ROM library read-only. Two things on it matter to RomM:

- The **Selkies web UI**, which is what your browser loads the stream from.
- The **broker API**, which is where RomM sends launch, save, state and disc commands. It's served under the container's `SUBFOLDER` on the same origin.

There's a working compose file at [`docker-compose.streaming.yml`](https://github.com/rommapp/romm/blob/master/docker-compose.streaming.yml) upstream. Note the image is amd64 only.

### Set up `config.yml`

Add a `streaming` block with **one entry per container** (full schema in [Configuration File → `streaming`](../reference/configuration-file.md#streaming)). Whatever you set at the container level applies to every platform it serves, and a platform block only needs to name the things that differ.

```yaml
streaming:
    enabled: true
    containers:
        - protocol: webstation
          host: https://192.168.1.56:3010
          subfolder: /streaming
          label: Emulation station
          platforms:
              snes: retroarch # just the emulator name...
              ps2: # ...or a block overriding container keys
                  emulator: pcsx2
                  memory_card_sync: true
```

Four of those keys have consequences worth knowing before you pick their values:

- `host` is what the browser connects to, and it has to be **HTTPS**: Selkies WebRTC won't run without a secure context. Use the container's self-signed cert, or put it behind a [reverse proxy with TLS](../install/reverse-proxy.md). A path like `/streaming` works if you've proxied the container onto RomM's own origin, but then you must set `broker_host` yourself, because a bare path gives RomM no address to call.
- `broker_host` is only ever called server to server, so plain HTTP is fine. Pooled containers are identified by it, so two serving the same platform need different ones.
- `library_path` is where the container sees your library. Don't change it casually, since your state and save history is keyed to it.
- The per-platform `emulator` names what that platform's states and memory cards are filed under, so renaming it later orphans everything stored under the old name. A container-level `emulator` is ignored whenever `platforms` is used.

### Set the shared secret

`STREAMING_BROKER_SECRET` is what authenticates RomM to the broker, and it has to match the container's `BROKER_SECRET`. Use the **same value** everywhere.

If one broker needs its own secret, put `broker_secret` on that entry in `config.yml` and leave `STREAMING_BROKER_SECRET` unset entirely. The env var beats the per-container value whenever it's set, so you can't mix the two.

### Tune the timeouts

Three env vars bound how long streaming waits, listed with their defaults in [Environment Variables → Emulator Streaming](../reference/environment-variables.md#emulator-streaming).

`STREAMING_LAUNCH_TIMEOUT` covers the whole launch, including any unpacking before the emulator starts. `STREAMING_SAVE_TIMEOUT` covers save-and-exit, and needs raising if a broker's own `SAVE_WAIT` is higher. `STREAMING_STATE_HISTORY_LIMIT` caps how many states are kept per ROM, emulator and user.

## Troubleshooting

- **No stream action on a platform.** Either `streaming.enabled` is off, nothing is configured for that platform slug, or the config hasn't reloaded. RomM reads the streaming config when the app loads, so refresh the page after editing `config.yml`.
- **Stream never loads.** The browser can't reach `host`, or `host` isn't HTTPS. Open the Selkies URL directly in a browser from the client machine and see what happens.
- **Launch or save errors out.** Either the server can't reach `broker_host` or the secret is wrong. Check `STREAMING_BROKER_SECRET` matches on both sides, and that `broker_host` actually resolves from the server.
- **A container shows as unconfigured in the fleet.** Its `host` is missing a scheme, or RomM has no reachable broker for it. It can't be claimed until that's fixed.
- **Platform stuck as in use.** Someone disconnected without releasing it. Wait for the heartbeat to go stale or force-release it from the fleet.
- **"The previous session is still saving".** An exit is still pulling state off the container. Give it a moment and try again.
