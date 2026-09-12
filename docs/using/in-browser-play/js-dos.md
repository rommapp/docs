---
title: js-dos
description: Play Windows 3.x and 9x games in the browser via DOSBox-X
---

# `js-dos`

[`js-dos`](https://js-dos.com/) runs DOSBox-X in the browser for Windows 3.x (`win3x`) and Windows 9x (`win9x`) titles. MS-DOS games continue to use the [EmulatorJS `dosbox-pure` core](ms-dos.md).

<!-- prettier-ignore -->
!!! info "Bundled in the full image, fetched from a CDN in slim"
    The full container image ships the `js-dos` runtime locally. The slim image has no local copy, so the player falls back to jsDelivr at runtime and needs outbound internet access from the browser (see [Image Variants](../../install/image-variants.md)).

<!-- prettier-ignore -->
!!! warning "`js-dos` requires HTTPS"
    DOSBox-X uses the `SharedArrayBuffer` API, which browsers only expose in secure, cross-origin-isolated contexts, so RomM must be served over `https://` for these games to run. Use a [reverse proxy with TLS](../../install/reverse-proxy.md) if you're still on plain HTTP.

Server owners can turn the player off with `DISABLE_JSDOS=true` (see [Environment Variables](../../reference/environment-variables.md)).

## Bundling a game

RomM passes the selected file directly to `js-dos`, so upload a ready-to-run [`js-dos` bundle](https://js-dos.com/jsdos-bundle.html), not a regular zip of loose game files. The bundle is a zip archive carrying a `.jsdos/dosbox.conf`, and RomM only offers the player for files with a `.jsdos` extension, so rename the archive before uploading:

```text
game.jsdos
    .jsdos/
        dosbox.conf
    WINDOWS/
    ...game files
```

<!-- prettier-ignore -->
!!! important "The file extension must be `.jsdos`"
    A bundle left as `game.zip` scans in fine but never gets a Play button, because RomM gates the `js-dos` player on the file extension.

The configuration controls how the bundle boots. For example, a Windows 3.x bundle with Windows installed in the bundle root can use:

```ini
[dosbox]
machine=svga_s3
memsize=32

[autoexec]
@echo off
mount c .
c:
WIN GAMEDIR\GAME
```

- `mount c .` mounts the bundle root as `C:`. `js-dos` does not add this mount automatically.
- `WIN GAMEDIR\GAME` boots Windows straight into the game instead of Program Manager.

Windows 9x and disk-image layouts need different DOSBox-X configuration. Use the [`js-dos` bundle cookbook](https://js-dos.com/jsdos-bundle.html) or [`js-dos` Game Studio](https://v8.js-dos.com/studio/), its browser-based bundle builder. Upload the result under the `win3x` or `win9x` platform. RomM uses `js-dos` only for those platforms and leaves `dos` with EmulatorJS.

## Saves

`js-dos` stores filesystem changes in the browser, isolated by RomM user and game. They are not uploaded or synced with RomM. Quitting the player writes a final save, so wait for it to finish rather than closing the tab mid-game.

<!-- prettier-ignore -->
!!! warning "Saving depends on the application"
    Some applications save only when you exit back to Windows. Exit the application before quitting the player.
