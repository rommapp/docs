---
title: Saves & States
description: Manage save files and save-states across in-browser play and synced devices
---

# Saves & States

Save files and save states are two different things that are easy to confuse:

- **Save files**: the in-game save (`.srm`, `.sav`, `.save`, etc.), which the game writes when you use its in-game save feature. Save files work across emulator cores that share the format.
- **Save states**: a full memory snapshot of the emulator at a moment in time. States are emulator-specific, so a SNES9x state won't load in bsnes.

Both are kept per user and per ROM, stored under `/romm/assets/<user>/<rom>/`. They follow you across browsers and devices.

## Uploading

You can upload save files for your own games (handy for importing from real hardware via Retrode/GB Operator or from another emulator). States upload the same way, with an optional screenshot attachment that's generated automatically when the state is created from in-browser play.

## Selecting on launch

If a ROM has multiple saves or states, RomM presents a picker before the emulator loads.

## In-emulator behaviour

Saves and states you create in the emulator are written straight back to the server, so there's no "forgot to upload" step. The player also asks you to confirm before navigating away from a running game, so you don't lose unsaved progress.

In-game, the Export and Import save buttons are replaced by a single **Load save or state** picker, which opens with the same Saves and States tabs as the launch screen. A state applies on the fly, while picking a save restarts the game from that save. Either one replaces what's running, so you're asked to confirm first.

A **Sync save** button appears alongside it when [automatic save sync](#automatic-save-sync) is off, to upload the current save on demand.

## Automatic save sync

A save syncs automatically with the server seconds after it's stored in the browser. The player watches the emulator's SRAM while you play and uploads a new version as soon as one appears, so your progress is saved even if the tab is closed or the browser crashes. Leaving the player uploads anything the server doesn't have yet.

This is on by default. Set [`emulatorjs.auto_save_sync`](../reference/configuration-file.md#emulatorjsauto_save_sync) to `false` to go back to uploading only on **save and quit**:

```yaml
emulatorjs:
    auto_save_sync: false
```

Each upload is the entire save file, and some games save constantly. On a small instance you won't notice, but you might with a lot of users and large saves. This is instance-wide, set by the server owner, and only affects in-browser play. Save states already upload as you create them and aren't affected either way.

An upload the server doesn't take (it's down, the connection dropped) is held in your browser with the screenshot taken when the game wrote it, and retried later. The player tells you whether it was kept, so a "kept for later" message means the progress is safe even though the save isn't on the server yet. Held saves belong to the account that made them, so a shared browser won't hand your progress to whoever signs in next.

## Save slots

Saves are organized into slots, the model the [sync clients](#syncing-saves-between-browsers-and-devices) use too, so you see the same slots whether you played in the browser or on a device.

- **`autosave`** is where ordinary play goes, and it keeps a capped history, so it prunes itself as you play.
- **A named slot**, created on launch, keeps every version. Use one when you want a checkpoint you can always come back to.

Each slot lists its newest version first, tagged **Latest**, with older versions folded behind a toggle. A version written in the browser carries a screenshot from the moment it was written, shown as its thumbnail.

The server prunes a slot to `MAX_SAVES_PER_SLOT` (50 by default, `0` to disable the cap). A client that asks for a tighter limit of its own gets the tighter of the two. Saves uploaded without a slot, such as one you imported by hand, are never pruned.

## Syncing saves between browsers and devices

Every in-browser player ([EmulatorJS](in-browser-play/emulatorjs.md), [EasyRPG](in-browser-play/easyrpg.md), [`js-dos`](in-browser-play/js-dos.md), [PICO-8](in-browser-play/pico-8.md) and [Ruffle](in-browser-play/ruffle.md)) syncs saves the same way a handheld does. Each browser profile registers as one of your [devices](devices.md), and when a game launches it negotiates its saves with the server: it downloads what's newer on the server, uploads what's newer locally, and drops a save that was deleted on the server.

When both sides changed the same slot, the browser plays the server's copy and uploads its own as a separate archived save, named after the game and the time it was captured, so neither version is lost. A browser only pairs saves written by its own player and leaves a save from another emulator in the same slot alone.

Saves and states also sync with companion apps on other devices (Grout on muOS, Argosy on Android, DeckRommSync on a Deck, etc.), and with [RetroArch](../ecosystem/retroarch-cloud-sync.md) through its built-in Cloud Sync. These pages cover it in depth:

- [Devices](devices.md): registering, renaming and removing them
- [RetroArch Cloud Sync](../ecosystem/retroarch-cloud-sync.md): setup and what syncs
- [Device Sync Protocol](../developers/device-sync-protocol.md): wire-level reference
- [SSH Sync](../developers/ssh-sync.md): server owner config
- [Argosy Launcher](../ecosystem/first-party-apps.md#argosy-launcher)/[Grout](../ecosystem/first-party-apps.md#grout): per-app setup

Once a device is paired and sync is running, saves made on it appear server-side on its next sync. When the same slot is saved on two devices between syncs, RomM reports the conflict to the app, which decides what to keep, and most apps keep both as separate save entries.

## Favorites, labels and names

You can mark your own saves and states as favorites and tag them with free-text labels, for example to name a run or flag the save before a boss. A save or state takes up to 20 labels of up to 255 characters each, and labels that differ only in case count as one. You can also favorite, label or delete several at once.

A save or state can be renamed, and its screenshot follows it. The new name has to be free among that game's saves (or states), ignoring case, and keep a name before the extension. A device or RetroArch that syncs by file name sees a renamed file as a different file.

Saves and states written in the browser are named after the game and the local time they were captured, so the timestamp in the name matches your clock.

When you share a save or state with other users, they see its author but not its favorite flag or labels, which stay yours.

## Format/core compatibility

### Saves

Save files are usually format-interchangeable across cores for the same platform but not always.

| Platform           | Format                 | Usually-compatible                                |
| ------------------ | ---------------------- | ------------------------------------------------- |
| NES                | `.sav`                 | Yes, across FCEUmm/Nestopia                       |
| SNES               | `.srm`                 | Yes, across SNES9x/bsnes                          |
| Genesis/Mega Drive | `.srm`                 | Yes                                               |
| Game Boy/GBC/GBA   | `.sav`                 | Yes, across Gambatte/mGBA                         |
| N64                | `.srm`, `.eep`, `.fla` | Yes but per-type: the right file must be uploaded |
| PSX                | `.srm` (memory card)   | Yes, across Mednafen/PCSX cores                   |
| Saturn/Dreamcast   | Varies                 | Check core docs                                   |

If you're moving saves between the bundled EmulatorJS and a stand-alone emulator (RetroArch, Dolphin, PPSSPP), it usually works for mainline cores.

### States

Save states are always core-specific (a SNES9x state will not load in bsnes), so switching cores leaves your existing states unusable.

States made through [emulator streaming](emulator-streaming.md) record the RetroArch core that wrote them. When you resume from a state another core wrote, such as after a per-platform core override, the container starts the game fresh instead of loading a state its core can't read. States from before cores were recorded count as the platform's default core.

If you use states heavily, stick to one core per platform, or use save files (which are interchangeable) as your primary persistence.

## RetroAchievements and states

If you use [RetroAchievements](retroachievements.md) in hardcore mode, loading a save state disables achievement tracking for that session. This isn't enforced locally but the RA server will stop crediting achievements. Use save files (the in-game save) instead of states if you care.

## Troubleshooting

- **Save uploaded but the game doesn't see it**: wrong format for the core. Check the compatibility table above, then re-upload or switch cores.
- **State loads a corrupted frame**: state was saved by a different build of the core. If the emulator bundle updated, old states may not load cleanly. Re-create or start a fresh save.
- **Save disappears after play**: the emulator didn't write a save at all. Use the in-game save feature rather than relying on the emulator flushing on its own, and check that [automatic save sync](#automatic-save-sync) is on.
- **Can't upload, "file too large"**: reverse proxy limit. Raise `client_max_body_size`/`proxy-body-size` (see [Reverse Proxy](../install/reverse-proxy.md)).

More in [Troubleshooting](../troubleshooting/index.md).
