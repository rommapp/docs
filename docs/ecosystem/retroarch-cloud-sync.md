---
title: RetroArch Cloud Sync
description: Use RomM as the WebDAV target for RetroArch's built-in Cloud Sync
---

# RetroArch Cloud Sync

RetroArch has a built-in Cloud Sync feature that mirrors its saves, states and other folders to a WebDAV server. RomM can be that server, so RetroArch syncs directly into your library without a companion app.

Each save and state is attached to the ROM it belongs to, next to the ones from the web player and other [devices](../using/devices.md).

## Requirements

- A RetroArch build with Cloud Sync and the WebDAV driver (desktop, Android and most handheld builds have it)
- A RomM account with a password, since RetroArch signs in with HTTP Basic auth and an account that only signs in through [OIDC](../administration/oidc/index.md) has none to send
- Your ROM files named the same on both sides, because that's how RomM tells which game a save belongs to (see [How files match games](#how-files-match-games))

## Configure RetroArch

Point Cloud Sync at RomM's WebDAV path and sign in with your RomM username and password:

```text
https://romm.example.com/api/sync/retroarch/
```

The trailing slash matters, because RetroArch appends its own paths to the URL as written.

You can set it in the Cloud Sync settings or directly in `retroarch.cfg`:

```ini
cloud_sync_enable = "true"
cloud_sync_driver = "webdav"
webdav_url = "https://romm.example.com/api/sync/retroarch/"
webdav_username = "your-romm-username"
webdav_password = "your-romm-password"

# What to sync
cloud_sync_sync_saves = "true"
cloud_sync_sync_configs = "true"
cloud_sync_sync_thumbs = "false"
cloud_sync_sync_system = "false"
```

We also recommend turning on RetroArch's options to sort saves and states into per-core folders (`sort_savefiles_enable` and `sort_savestates_enable`). RomM stores each save and state with the emulator that wrote it, and the per-core folder is how that emulator survives the round trip (see [Cores and folders](#cores-and-folders)).

## What syncs

| RetroArch folder | Where it goes in RomM                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| `saves/`         | A save on the matching ROM, for your user                                                       |
| `states/`        | A state on the matching ROM, for your user, with RetroArch's `.png` thumbnail as its screenshot |
| `config/`        | Stored as-is, per user                                                                          |
| `thumbnails/`    | Stored as-is, per user                                                                          |
| `system/`        | Stored as-is, per user                                                                          |

The `config`, `thumbnails` and `system` folders belong to no game, so RomM keeps them as opaque files under `/romm/retroarch_sync/users/<user>/` and hands them back unchanged to every RetroArch install signed in as that user. To RomM those installs are all one device, because RetroArch's requests don't say which install they come from. The first sync registers a single device named **RetroArch**, which shows up with the user's other [devices](../using/devices.md). RomM also ignores the `manifest.server` file RetroArch uploads and builds its own from the database on every sync, so RetroArch always compares against what RomM actually holds.

### Saves

RetroArch saves go through the same [save slots](../using/saves-and-states.md#save-slots) as the web player and other device-sync apps. For each game, core and file extension, RomM offers the newest save from any slot under the name RetroArch expects (`<game>.srm`, for example), so progress made in the browser or on another device reaches RetroArch, and the other way around.

Each upload adds a new version to the slot of the save RetroArch was offered, or to `autosave` when there was none. An upload with the same bytes as the newest version adds nothing. The slot keeps up to `MAX_SAVES_PER_SLOT` versions for that core and extension, so a `.rtc` file or another core's save in the same slot keeps its own history.

A save stored without a slot, such as one you uploaded by hand, is offered until the first upload for that game and core files a slotted version.

### States

RetroArch only loads states from its numbered slots (`<game>.state`, `<game>.state1` and so on, plus `<game>.state.auto`). RomM groups every state for a game by core and by the slot its file name ends in, and offers the newest one in each slot under the name RetroArch would give it.

A state made in RomM's web player has a label and a timestamp in its name instead of a slot number, but it still ends in `.state`, so RomM offers it as that game's slot 0 when it's the newest state there, and RetroArch loads it like any other.

### Deletes

Deleting a save or state in RetroArch deletes it in RomM too. For a save, that's every version RomM could offer in its place (the game's slotted saves for that core and extension in every slot, plus the unslotted save at that path), so no older version comes back on the next sync. In non-destructive mode RetroArch moves a deleted file into a `deleted/` folder instead, and RomM treats that move as a delete as well, since keeping the row would push the file straight back on the next sync.

## How files match games

A synced file names no platform or ROM, so RomM matches it by file name. The save or state's name, minus its extension (and minus the `.state`, `.stateN` or `.state.auto` suffix for a state), has to equal a ROM's file name without its extension. RetroArch names saves after the content file it loaded, so this works as long as the ROM is named the same on the device and in RomM.

- `saves/Snes9x/Super Mario World (USA).srm` matches the ROM file `Super Mario World (USA).sfc`
- `states/Snes9x/Super Mario World (USA).state2` matches the same ROM, in slot 2

The match prefers the exact spelling and falls back to a case-insensitive one. Only ROMs you can see count, and when two visible ROMs on different platforms share a name, the one with the lowest ID wins.

An upload that matches no ROM is refused with `409`, and a `Cloud sync upload ... matches no ROM in the library` warning is logged. RetroArch reports the sync as failed for that file and tries again next time.

### Cores and folders

With saves and states sorted by core, RetroArch puts them in folders named after the core, such as `saves/Snes9x/`. RomM maps the common RetroArch folder names to the core IDs its web player uses, so a state from the web player's `snes9x` core shows up in RetroArch's `Snes9x` folder and the other way around. A folder name that isn't recognized is stored unchanged as the emulator name.

## PSP saves

PPSSPP keeps each game's save as a folder of files under `PSP/SAVEDATA/<folder>/`, and those files only make sense together. RomM bundles each folder into one zipped save on the matching ROM, named `PSP-<folder>.zip`, and unpacks it again when RetroArch downloads it. Files under `PSP/SYSTEM/` are PPSSPP's own caches and are ignored.

The ROM for a save folder is found in two ways:

1. **From `SYNC_RETROARCH_PSP_SERIAL_MAP`**, if the folder's serial is listed there
2. **From the title in the folder's `PARAM.SFO`**, compared against your ROMs' names with punctuation and case ignored

The serial is the folder name with any trailing `DATA<n>` dropped, so `ULUS10041DATA00` has the serial `ULUS10041`. Until one of those finds a ROM, the folder's files are held in the cache and retried when the rest of the folder arrives.

When a game's title doesn't match the ROM's name, as with a translated title or a ROM renamed by hand, map its serial to the ROM's file name without the extension:

```yaml
environment:
    SYNC_RETROARCH_PSP_SERIAL_MAP: '{"ULUS10041": "Lumines (USA)", "NPJH50465": "Persona 3 Portable (Japan) (En)"}'
```

Whenever a folder can't be matched, the serial to add is logged.

## Browsing with other WebDAV clients

The same path works read-only in generic WebDAV clients, such as a file manager that mounts WebDAV shares:

- `roms/` lists your platforms and their ROM files. Opening a file redirects to the normal [download endpoint](../using/downloads.md), so range requests and multi-file ZIPs behave the same way.
- `saves/` and `states/` list the same files RetroArch sees.

Reading anything needs the `assets.read` permission, and browsing `roms/` also needs `roms.read` and shows only the platforms and games you can see. With [kiosk mode](../administration/authentication.md#kiosk-mode) on, anonymous visitors can browse `roms/` without signing in, but `saves/` and `states/` still ask for credentials. Changes (`PUT`, `DELETE`, `MOVE`, `MKCOL`) need `assets.write`. `LOCK` and `UNLOCK` always succeed, because some clients refuse to mount a share without a lock.

## Reverse proxy

WebDAV is served under `/api/sync/retroarch/`, so a proxy that already forwards `/api` covers it, as long as it lets these methods through:

```text
OPTIONS, PROPFIND, GET, HEAD, PUT, DELETE, MKCOL, MOVE, LOCK, UNLOCK
```

Most proxies forward any method, but some web application firewalls and CDN rules block the WebDAV ones. The proxy also has to pass the `Authorization` header through and accept upload bodies as large as your biggest save or state (see [Reverse Proxy](../install/reverse-proxy.md)).

## Troubleshooting

- **RetroArch says the sync failed right away**: check the URL ends in `/api/sync/retroarch/`, with the trailing slash, and that the username and password sign in to the RomM web UI.
- **A save never shows up in RomM**: its file name matches no ROM you can see. Look for a `matches no ROM in the library` warning in the logs, then rename the ROM or the save so they agree.
- **A web player state doesn't show up in RetroArch**: only the newest state per slot is offered, so a newer state in the same slot hides it. RetroArch also has to be sorting states by core for the state to land in the folder the core reads from.
- **A browser save doesn't show up in RetroArch**: only the newest save for the game, core and extension is offered (see [Saves](#saves)), and it lands in the folder of the core that wrote it. Check that RetroArch sorts saves by core and runs the same core as the browser player.
- **A PSP save doesn't sync**: the folder's title didn't match a ROM. Add the serial from the log message to `SYNC_RETROARCH_PSP_SERIAL_MAP` and restart RomM.
- **Errors only on `PROPFIND`, `MOVE` or `MKCOL` requests**: something in front of RomM blocks WebDAV methods (see [Reverse proxy](#reverse-proxy)).
- **Large states fail to upload**: raise your proxy's body size limit.

## See also

- [Saves & States](../using/saves-and-states.md): how they're stored
- [Devices](../using/devices.md): the RetroArch device and the others you sync from
- [Device Sync Protocol](../developers/device-sync-protocol.md): the API that companion apps sync over instead
