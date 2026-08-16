---
title: js-dos
description: Play Windows 3.x and 9x games in the browser via DOSBox-X
---

# `js-dos`

[`js-dos`](https://js-dos.com/) runs DOSBox-X in the browser for Windows 3.x (`win3x`) and Windows 9x (`win9x`) titles. MS-DOS games continue to use the [EmulatorJS `dosbox-pure` core](ms-dos.md).

<!-- prettier-ignore -->
!!! important "The full image is required"
    `js-dos` is bundled only with RomM's full container image. The slim image has no `js-dos` CDN fallback. See [Image Variants](../../install/image-variants.md).

## Bundling a game

RomM passes the selected file directly to `js-dos`, so upload a ready-to-run [`js-dos` bundle](https://js-dos.com/jsdos-bundle.html), not a regular zip of loose game files. The bundle is a zip with a required `.jsdos/dosbox.conf`:

```text
game.zip
    .jsdos/
        dosbox.conf
    WINDOWS/
    ...game files
```

The configuration controls how the bundle boots. For example, a Windows 3.x bundle with Windows installed in the zip root can use:

```ini
[dosbox]
machine=svga_s3
memsize=32

[autoexec]
echo off
mount c .
c:
WIN GAMEDIR\GAME
```

- `mount c .` mounts the bundle root as `C:`. `js-dos` does not add this mount automatically.
- `WIN GAMEDIR\GAME` boots Windows straight into the game instead of Program Manager.

Windows 9x and disk-image layouts need different DOSBox-X configuration. Use the [`js-dos` bundle cookbook](https://js-dos.com/jsdos-bundle.html) or [`js-dos` Game Studio](https://v8.js-dos.com/studio/), its browser-based bundle builder. Upload the result under the `win3x` or `win9x` platform. RomM uses `js-dos` only for those platforms and leaves `dos` with EmulatorJS.

## Saves

`js-dos` stores filesystem changes in the browser, isolated by RomM user and game. They are not uploaded or synced with RomM. Use **Quit** and wait for the final save before leaving the player.

<!-- prettier-ignore -->
!!! warning "Saving depends on the application"
    Some applications save only when you exit back to Windows. Exit the application before quitting the player.
