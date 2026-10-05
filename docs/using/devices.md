---
title: Devices
description: The browsers, handhelds and apps your saves sync with, and installing games on them
---

# Devices

A device is anything that syncs saves with RomM on your behalf: a handheld running [Grout](../ecosystem/first-party-apps.md#grout), a phone running [Argosy](../ecosystem/first-party-apps.md#argosy-launcher), [RetroArch](../ecosystem/retroarch-cloud-sync.md), or a web browser you play in. Each device belongs to one user, and RomM tracks which version of each save every device last synced, which is how it tells an ordinary update apart from a conflict.

Your devices are listed at `/devices`, where you can rename a device, turn sync off for it, or remove it.

## Browsers are devices too

All five in-browser players ([EmulatorJS](in-browser-play/emulatorjs.md), [EasyRPG](in-browser-play/easyrpg.md), [`js-dos`](in-browser-play/js-dos.md), [PICO-8](in-browser-play/pico-8.md) and [Ruffle](in-browser-play/ruffle.md)) sync saves through device sync. Each browser profile registers itself as a device the first time you play, named after the browser and OS, such as "Firefox on macOS", so a second browser, or a second profile in the same browser, is a separate device.

When a game launches, the browser negotiates its saves with the server, the same way a handheld does at the start of a sync (see [Saves & States](saves-and-states.md#syncing-saves-between-browsers-and-devices)). A save made in one browser is waiting in another, and when both changed the same slot, the browser plays the server's copy and archives its own so neither is overwritten.

A browser keeps its saves in local storage until they reach the server. Because that storage can be cleared or evicted, a save the browser no longer holds is treated as lost rather than deleted, and the server offers it back on the next launch.

An account without the `devices.write` permission can't register devices, so its browsers keep their saves locally and skip device sync.

## Managing devices

- **Renaming** changes only the name RomM shows, for example to tell two handhelds of the same model apart.
- **Turning sync off** makes RomM refuse that device's sync requests, so nothing moves in either direction until you turn it back on, and a browser with sync off keeps its saves locally.
- **Removing** a device deletes it, its sync history and any installs queued for it, but the saves it uploaded stay on the server. A browser registers itself again the next time you play in it, and an app re-registers on its next sync, so removing is mostly for cleaning up a device you no longer use.

## Install on device

You can send a game to one of your devices, and RomM adds it to that device's download queue for the device to fetch the next time it's online.

Only devices whose app reports that it accepts installs are offered, which leaves out browsers and RetroArch. RomM also shows whether each device is online, meaning it holds an open connection to RomM's `/devices` socket, which a supporting app keeps open while it runs.

A request waits in the device's queue until the device takes it and reports back. You get a [notification](notifications.md) when it finishes or fails, and you can cancel a request any time before it finishes. A request nothing picks up expires after `DEVICE_INSTALL_REQUEST_TTL_DAYS` days without a change (2 by default).

The device receives the game's own files, along with any update and DLC files in its folder, but not manuals or other extras. A game with none of those files on disk can't be installed.

### Server settings

| Variable                                 | Default                        | Description                                                                |
| ---------------------------------------- | ------------------------------ | -------------------------------------------------------------------------- |
| `DEVICE_INSTALL_ENABLED`                 | `true`                         | Turn installs on or off for everyone                                       |
| `DEVICE_INSTALL_REQUEST_TTL_DAYS`        | `2`                            | Days an unfinished request waits after its last change (`0` waits forever) |
| `DEVICE_INSTALL_EXCLUDED_PLATFORM_SLUGS` | `win,win3x,win9x,windows-apps` | Comma-separated platform slugs that can never be sent to a device          |

Install requests live in Valkey rather than the database, so they're lost if Valkey loses its data, and devices then see an empty queue.

Apps that accept installs follow the request lifecycle and `/devices` socket events described in the [Device Sync Protocol](../developers/device-sync-protocol.md#installs-on-devices).

## See also

- [Saves & States](saves-and-states.md): how they sync
- [RetroArch Cloud Sync](../ecosystem/retroarch-cloud-sync.md): saves and states over WebDAV
- [Client API Tokens](../developers/client-api-tokens.md): how apps pair with RomM
