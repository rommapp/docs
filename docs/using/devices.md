---
title: Devices
description: The browsers, handhelds and apps your saves sync with, and installing games on them
---

# Devices

A device is anything that syncs saves with RomM on your behalf: a handheld running [Grout](../ecosystem/first-party-apps.md#grout), a phone running [Argosy](../ecosystem/first-party-apps.md#argosy-launcher), [RetroArch](../ecosystem/retroarch-cloud-sync.md), or a web browser you play in. Each device belongs to one user, and RomM tracks which version of each save every device last synced, which is how it tells an ordinary update apart from a conflict.

Your devices are listed at `/devices`. From there you can rename a device, turn sync off for it, or remove it.

## Browsers are devices too

All five in-browser players ([EmulatorJS](in-browser-play/emulatorjs.md), [EasyRPG](in-browser-play/easyrpg.md), [`js-dos`](in-browser-play/js-dos.md), [PICO-8](in-browser-play/pico-8.md) and [Ruffle](in-browser-play/ruffle.md)) sync saves through device sync. Each browser profile registers itself as a device the first time you play, named after the browser and OS, such as "Firefox on macOS". A second browser, or a second profile in the same browser, is a separate device.

When a game launches, the browser negotiates its saves with the server, the same way a handheld does at the start of a sync (see [Saves & States](saves-and-states.md#syncing-saves-between-browsers-and-devices)). A save made in one browser is waiting in another, and when both changed the same slot, the browser plays the server's copy and archives its own instead of overwriting either.

Saves a browser holds stay in its storage until they reach the server. A browser's storage can be cleared or evicted, so a save it no longer holds is treated as lost rather than deleted, and the server offers it back on the next launch.

An account without the `devices.write` permission can't register devices, so its browsers keep their saves locally and skip device sync.

## Managing devices

- **Renaming** changes only the name RomM shows, for example to tell two handhelds of the same model apart.
- **Turning sync off** makes RomM refuse that device's sync requests, so nothing moves in either direction until you turn it back on. Saves in a browser with sync turned off stay in that browser.
- **Removing** a device deletes it and its sync history, and drops any installs queued for it. The saves it uploaded stay on the server. A browser registers itself again the next time you play in it, and an app re-registers on its next sync, so removing one is mostly useful to clean up a device you no longer use.

## Install on device

You can send a game from RomM to one of your devices. RomM adds it to that device's download queue, and the device downloads it the next time it's online.

Only devices whose app reports that it accepts installs are offered, so browsers and RetroArch never are. RomM also shows whether each device is online right now. A device counts as online while it holds an open connection to RomM's `/devices` socket, which a supporting app keeps open while it runs.

A request waits in the device's queue until the device takes it and reports back. You get a [notification](notifications.md) when it finishes or fails, and you can cancel a request any time before it finishes. A request nothing picks up expires after `DEVICE_INSTALL_REQUEST_TTL_DAYS` days without a change (2 by default).

The device receives the game's own files, along with any update and DLC files in the game's folder. Manuals and other extras aren't sent. A game with none of those files on disk can't be installed.

### Server settings

| Variable                                 | Default                        | Description                                                                |
| ---------------------------------------- | ------------------------------ | -------------------------------------------------------------------------- |
| `DEVICE_INSTALL_ENABLED`                 | `true`                         | Turn installing on devices on or off for everyone                          |
| `DEVICE_INSTALL_REQUEST_TTL_DAYS`        | `2`                            | Days an unfinished request waits after its last change (`0` waits forever) |
| `DEVICE_INSTALL_EXCLUDED_PLATFORM_SLUGS` | `win,win3x,win9x,windows-apps` | Comma-separated platform slugs that can never be sent to a device          |

Install requests live in Valkey rather than the database, so they're lost if Valkey loses its data, and devices simply see an empty queue.

Building an app that accepts installs? The request lifecycle and the `/devices` socket events are in the [Device Sync Protocol](../developers/device-sync-protocol.md#installs-on-devices).

## See also

- [Saves & States](saves-and-states.md): how saves and states sync
- [RetroArch Cloud Sync](../ecosystem/retroarch-cloud-sync.md): syncing RetroArch with RomM
- [Client API Tokens](../developers/client-api-tokens.md): how apps pair with RomM
