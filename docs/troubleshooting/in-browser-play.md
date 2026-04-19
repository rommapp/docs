---
title: In-Browser Play Troubleshooting
description: Diagnose EmulatorJS and Ruffle issues: cores not loading, BIOS missing, audio, performance.
---

# In-Browser Play Troubleshooting

## EmulatorJS won't load at all

Symptom: Play button spins forever or shows an error immediately.

Checks in order:

1. **Is it the slim image?** `ENABLE_EMULATORJS=true` on the slim image doesn't magically include EmulatorJS. Either switch to `rommapp/romm:<version>` (full) or disable in-browser play. See [Image Variants](../install/image-variants.md).
2. **Browser console**: open devtools, look for 404s on `/assets/emulatorjs/...`. Indicates the EmulatorJS bundle didn't install correctly in the container. `docker logs romm` may show the entrypoint's install step failing.
3. **Browser compatibility**: EmulatorJS uses SharedArrayBuffer. Needs a modern Chrome/Firefox/Safari and an HTTPS-served RomM (cross-origin isolation requires HTTPS). If you're still on plain HTTP for some reason, TLS it. See [Reverse Proxy](../install/reverse-proxy.md).

## Black screen, no audio

EmulatorJS loaded, but the game is dead.

- **Core incompatibility.** Some cores have issues with specific ROMs. Try a different core via in-game Menu → **Core**.
- **ROM dump is bad.** A broken dump produces a black screen on most emulators. Try a known-good No-Intro / Redump version.
- **Browser doesn't support WebGL.** Rare on modern browsers. Check `chrome://gpu` / `about:support` for WebGL status.

## "Firmware required"

The platform needs BIOS files RomM doesn't have. See [Firmware Management](../administration/firmware-management.md) for how to upload.

Specific examples:

- PlayStation → `scph1001.bin` (or region equivalents).
- Game Boy Advance → `gba_bios.bin`.
- Saturn → `saturn_bios.bin` + CD BIOS.
- Nintendo DS → `firmware.bin` + `bios7.bin` + `bios9.bin`.

Not sure which files? Error message usually names them. Or check [EmulatorJS Systems docs](https://emulatorjs.org/docs/systems/).

Multi-file firmware: zip them together and upload as a single `firmware.zip`. EmulatorJS unpacks automatically.

## Controls do nothing

- **Browser needs focus.** Click the emulator canvas once. Some cores need a button press to enumerate gamepads.
- **Gamepad not detected.** Chrome sometimes requires a button press on the page before it registers a gamepad. Press something on the pad.
- **Conflicting gamepad.** You have two gamepads plugged in and EmulatorJS is talking to the wrong one. Unplug the extras.
- **Keyboard mapping overrides.** In-game Menu → **Controls** → **Reset to Defaults**.

## Audio stutters / desyncs

- **Underpowered device.** Cheap TV boxes and old phones struggle. Try a lighter core (e.g. `snes9x` instead of `bsnes`), or accept the stutter.
- **Tab is backgrounded.** Most browsers throttle background tabs. Keep the play tab foregrounded.
- **Other tabs eating CPU.** Close them.
- **Specific to a core.** `mednafen_saturn` is notorious. Try `yabause` if Saturn audio is bad.

## Save states crash on load

- **Core changed between save and load.** States are emulator-build-specific. If RomM updated and your state was saved against the old build, it likely won't load. Start fresh, or switch to in-game saves (portable across builds).
- **Cheats on during save, off during load.** Or vice versa. Toggle to match.

## In-game Menu won't open

Different cores use different hotkeys:

- **PC keyboard**: often F1, F9, or `~` (tilde). Some cores use ESC.
- **Gamepad**: usually Select + Start simultaneously.

Rebind via Profile → User Interface (the operator-side overrides live in [`emulatorjs.controls`](../reference/configuration-file.md#emulatorjscontrols) in `config.yml`).

## DOS games fail to boot

- **autorun.bat issues**: turn on [`emulatorjs.disable_batch_bootup: true`](../reference/configuration-file.md#emulatorjsdisable_batch_bootup) in `config.yml`.
- **Sound card config wrong**: dosbox-pure tries to auto-detect, but may need manual tweaking. In-game Menu → **Settings** → set Sound Blaster port.
- **Game needs specific CPU speed**: some DOS games are CPU-bound. Slow down via dosbox-pure settings.

See the [MS-DOS platform guide](../platforms/ms-dos.md) for deeper DOS-specific notes.

## Ruffle games

- **"File not Flash"**: confirm the file extension is `.swf`. Ruffle only handles Flash SWF.
- **Wrong platform folder.** Ruffle only plays from `flash/` or `browser/` folders. See [Ruffle setup](../using/in-browser-play.md#ruffle).
- **AS3 game crashes**: Ruffle's ActionScript 3 support is in progress. Some games won't work cleanly yet. [Ruffle compatibility list](https://ruffle.rs/#compatibility).

## Performance on mobile

In-browser emulation is CPU-heavy. Mobile tips:

- **Plug the device in.** Batteries throttle. Playing plugged in gets you ~30% more performance.
- **Use Chrome on Android, Safari on iOS.** Other browsers are measurably slower for WASM.
- **Close other tabs.**
- **Try a lighter core.** `snes9x` over `bsnes`, `fceumm` over `nestopia`, etc.
- **Consider a native app.** [Argosy Launcher](../ecosystem/argosy.md) on Android uses native emulators, which are orders of magnitude more efficient.

## Fullscreen oddities

- **Notch / cutout clipping on mobile**: iPhone notches and Android cutouts can eat corners of the emulator viewport. Rotate to landscape before going fullscreen, or toggle Profile → User Interface → Fullscreen strategy.
- **Browser escapes fullscreen after idle**: browser security behaviour. Can't be worked around.

## Known limitations by core

| Core                  | Known issues                                                                |
| --------------------- | --------------------------------------------------------------------------- |
| `ppsspp` (PSP)        | Not supported in Console Mode.                                              |
| `dosbox-pure` (DOS)   | Not supported in Console Mode. Some DOS quirks. See `disable_batch_bootup`. |
| `mednafen_saturn`     | Audio stutter on weak hardware. `yabause` is an alternative.                |
| `opera` (3DO)         | Niche. Limited ROM compatibility.                                           |
| All Nintendo DS cores | Touchscreen emulation is imperfect on non-touch devices.                    |

## Still stuck

- `docker logs romm | grep -i emulator`: server-side clues.
- Browser devtools Console: client-side clues.
- [Discord](https://discord.gg/romm) `#help`: include the ROM file, the core you tried, the exact error.

For Netplay-specific issues: [Netplay Troubleshooting](netplay.md).
