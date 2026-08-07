---
title: js-dos
description: Play Windows 3.x and 9x games in the browser via DOSBox-X
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# js-dos

[js-dos](https://js-dos.com/) runs DOSBox-X in the browser and plays Windows 3.x (`win3x`) and 9x (`win9x`) titles that [EmulatorJS](emulatorjs.md) blank-screens. Native `dosbox-pure` (for example RetroArch) runs the same titles, so one bundle can carry both conventions.

## Bundling a game

Since the titles can be played in `dosbox-pure`, it is advisable to have the same title in `.zip` format bundling both `js-dos` and `dosbox-pure` conventions:
- `js-dos` reads a [js-dos bundle](https://js-dos.com/jsdos-bundle.html): a zip whose `.jsdos/dosbox.conf` holds an `[autoexec]` that mounts the drive and launches Windows. **js-dos does not auto-mount**.

<details>
<summary>.jsdos/dosbox.conf</summary>

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

</details>

- `mount c .` is required because js-dos will not mount for you.
- `WIN GAMEDIR\GAME` boots Windows straight into the game instead of Program Manager.
- CD titles: add `imgmount d GAME.iso -t iso`, or extract the ISO to a folder and `mount d CDFOLDER -t cdrom -label GAMECD` if a title rejects `imgmount`.

- `dosbox-pure` reads a root `DOSBOX.conf` (or `game.bat` and `setup.bat` for titles a bundled conf destabilizes). Its `[autoexec]` is the same minus `mount c .`, because `dosbox-pure` auto-mounts as `C:`.

```text
game.zip
    .jsdos/
        dosbox.conf
    DOSBOX.conf
    WINDOWS/
    ...game files
```

Each engine reads its own config and ignores the other. js-dos is only needed in the browser, where EmulatorJS blank-screens these titles. Native `dosbox-pure` runs the same bundle.

Upload the `.zip` under `win3x` or `win9x`. js-dos loads any zip containing `.jsdos/dosbox.conf`, so the same file also runs in native `dosbox-pure`. If you only need js-dos, omit the `dosbox-pure` config.

## Saves

js-dos auto-persists the emulated disk to your browser, so progress survives a reload. Saves are per-browser and per-game.

<!-- prettier-ignore -->
!!! info "Some apps only save on exit to Windows"
    A few titles such as Fine Artist only save when you exit the app back to Program Manager. Exit to Windows before quitting.

## Limitations

- RomM-synced saves are not enabled yet. This is intentional for now.

## Disabling the player

Set `DISABLE_JSDOS=true`, the same as `DISABLE_EMULATOR_JS` and `DISABLE_RUFFLE_RS` for the other players.

More in [In-Browser Play Troubleshooting](../../troubleshooting/in-browser-play.md).
