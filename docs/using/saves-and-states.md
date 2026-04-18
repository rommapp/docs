---
title: Saves & States
description: Manage save files and save-states across in-browser play and synced devices.
---

# Saves & States

Two different things, often confused:

- **Save files** — the in-game save (`.srm`, `.sav`, `.save`, etc.). What the game writes when you use the in-game save feature. Works across emulator cores that share the format.
- **Save states** — a full memory snapshot of the emulator at a moment in time. Emulator-specific; a SNES9x state won't load in bsnes.

Both are **per-user per-ROM** and stored under `/romm/assets/<user>/<rom>/`. They follow you across browsers and devices.

## Where to find them

Game detail page → **Game Data** tab. Separate sub-tabs for:

- **Saves** — all save files for this ROM, with date and emulator.
- **States** — all states, with thumbnail (if one was captured).

## Uploading a save

Useful for importing from real hardware (Retrode / GB Operator / etc.) or from another emulator.

1. Game detail → **Game Data** → **Upload Save**.
2. Drop the file.
3. Pick the emulator format if RomM can't infer it from the extension.
4. Save.

The save is available to [in-browser play](in-browser-play.md) on the next launch.

## Uploading a state

Same flow under **Upload State**. Optional screenshot attachment — RomM autogenerates one when you create a state from in-browser play; only matters when uploading from outside.

## Creating during play

In-game Menu in EmulatorJS:

- **Save** — writes in-game save data back to RomM. Same as the native console's save-to-cartridge flow.
- **Save State** / **Load State** — creates a full memory snapshot, or restores from one. RomM uploads the snapshot automatically.

There's no "forgot to upload" step — everything persists as soon as you do it in-emulator.

## Selecting on launch

If a ROM has multiple saves or states, the pre-launch picker appears before the emulator loads:

- **Save file** dropdown — which save to load on boot.
- **State** dropdown — optional; loads immediately after boot.

[Console Mode](console-mode.md) surfaces the same picker on a larger gamepad-friendly dialog.

## Downloading

For using a save on real hardware or another emulator elsewhere:

**Game Data → Saves → Context menu (…) → Download**.

Or bulk-download everything for a ROM by multi-selecting → toolbar → Download.

## Deleting

**Game Data → Saves/States → Context menu → Delete**. Removes both the DB row and the file. Can't be undone.

For bulk cleanup (e.g. "delete every state for games I've beaten"), use the multi-select toolbar.

## Device sync

Saves and states can sync to/from registered devices (Grout on muOS, DeckRommSync on a Deck, etc.). Covered in depth in the ecosystem section:

- [Device Sync Protocol](../ecosystem/device-sync-protocol.md) — wire-level reference.
- [SSH Sync](../administration/ssh-sync.md) — operator-side config.
- [Argosy Launcher](../ecosystem/argosy.md) / [Grout](../ecosystem/grout.md) — per-app setup.

From the end-user side: once your device is paired and sync is running, saves made on the device appear in RomM within a couple of sync cycles (default: 15 minutes). Conflicts — same ROM saved on two devices between syncs — surface as two separate save entries; pick which to keep.

## Format / core compatibility

### Saves

Save files are usually format-interchangeable across cores for the same platform, but not always.

| Platform | Format | Usually-compatible |
| --- | --- | --- |
| NES | `.sav` | Yes, across FCEUmm / Nestopia |
| SNES | `.srm` | Yes, across SNES9x / bsnes |
| Genesis / Mega Drive | `.srm` | Yes |
| Game Boy / GBC / GBA | `.sav` | Yes, across Gambatte / mGBA |
| N64 | `.srm`, `.eep`, `.fla` | Yes, but per-type — the right file must be uploaded |
| PSX | `.srm` (memory card) | Yes, across Mednafen / PCSX cores |
| Saturn / Dreamcast | Varies | Check core docs |

If you're moving saves between RomM's EmulatorJS and a stand-alone emulator (RetroArch, Dolphin, PPSSPP), usually works for mainline cores.

### States

Save states are **always** core-specific. A SNES9x state will not load in bsnes. If you switch cores, your states become useless.

Practical advice: stick to one core per platform if you use states heavily, or use save files (which are interchangeable) as your primary persistence.

## RetroAchievements and states

If you use [RetroAchievements](retroachievements.md) in hardcore mode, loading a save state **disables achievement tracking** for that session. RomM doesn't enforce this, but the RA server will stop crediting achievements. Use save files (the in-game save) instead of states if you care.

## Screenshots with states

When you create a state via in-game Menu → Save State, EmulatorJS grabs a frame as the state's thumbnail. Shows up in the **States** list and on the launch picker.

## Troubleshooting

- **Save uploaded but the game doesn't see it** — wrong format for the core. Check the compatibility table above; re-upload or switch cores.
- **State loads a corrupted frame** — state was saved by a different build of the core. If RomM updated the emulator bundle, old states may not load cleanly. Re-create or start a fresh save.
- **Save disappears after play** — the emulator didn't flush on quit. Use in-game **Save and Quit** instead of just closing the browser.
- **Can't upload — "file too large"** — reverse proxy limit; raise `client_max_body_size` / `proxy-body-size`. See [Reverse Proxy](../install/reverse-proxy.md).

More in [Troubleshooting](../troubleshooting/index.md).

## API

```http
POST   /api/saves                    # upload
GET    /api/saves                    # list own saves
GET    /api/saves/{id}/content       # download
PUT    /api/saves/{id}               # update metadata / attach screenshot
POST   /api/saves/delete             # bulk delete

POST   /api/states                   # upload
GET    /api/states                   # list own states
PUT    /api/states/{id}              # update
POST   /api/states/delete            # bulk delete
```

Requires `assets.read` / `assets.write` scopes. Full reference: [API Reference](../developers/api-reference.md).
