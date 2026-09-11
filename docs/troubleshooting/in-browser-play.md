---
title: In-Browser Play Troubleshooting
description: Diagnose EmulatorJS and Ruffle issues
---

# In-Browser Play Troubleshooting

## EmulatorJS won't load at all

- **On the slim image without internet?** The slim image fetches EmulatorJS cores from a CDN at runtime rather than bundling them, so without outbound network the browser can't load games. Either switch to the full image (cores bundled) or open outbound access (see [Image Variants](../install/image-variants.md)). Ruffle and PICO-8 have **no** CDN fallback whatsoever. Those two are full-image only.
- Check the **browser console** and look for 404s on `/assets/emulatorjs/...`, which indicate the EmulatorJS bundle didn't install correctly in the container. Check `docker logs romm` for entrypoint install-step failures.
- **Browser compatibility**: EmulatorJS uses SharedArrayBuffer, which needs a modern Chrome/Firefox/Safari and an HTTPS-served instance (cross-origin isolation requires HTTPS). If you're still on plain HTTP, set up TLS first (see [Reverse Proxy](../install/reverse-proxy.md)).

## "This core needs a secure connection"

Threaded cores need the `SharedArrayBuffer` API, and browsers only hand that out on a secure, cross-origin-isolated origin. Over plain HTTP the player now tells you this directly instead of throwing a generic error at you.

Fix it by serving RomM over `https://` (see [Reverse Proxy](../install/reverse-proxy.md)), or pick a single-threaded core for the platform. It comes up with the PSP core, with [`js-dos`](../using/in-browser-play/js-dos.md) for Windows 3.x and 9x, and with a few of the heavier EmulatorJS cores.

## Black screen or no audio

- **Core incompatibility.** Some cores have issues with specific ROMs. Try a different core via in-game Menu → **Core**.
- **ROM dump is bad.** A broken dump produces a black screen on most emulators. Try a known-good No-Intro/Redump version.
- **Browser doesn't support WebGL.** Rare on modern browsers. Check `chrome://gpu`/`about:support` for WebGL status.

## "Firmware required"

The platform needs BIOS files, so upload them via [Firmware Management](../administration/firmware-management.md).

Not sure which files you need? The error message usually names them, otherwise check the [EmulatorJS Systems docs](https://emulatorjs.org/docs/systems/). For multi-file firmware, zip the files together and upload as a single `firmware.zip`, which EmulatorJS unpacks automatically.

## Controls do nothing

- **Browser needs focus.** Click the emulator canvas once (some cores need a button press to enumerate gamepads).
- **Gamepad not detected.** Chrome sometimes requires a button press on the page before it registers a gamepad. Press something on the pad.
- **Conflicting gamepad.** You have two gamepads plugged in and EmulatorJS is talking to the wrong one. Unplug the extras.
- **Keyboard mapping overrides.** In-game Menu → **Controls** → **Reset to Defaults**

## Audio stutters/desyncs

- **Underpowered device.** Cheap TV boxes and old phones struggle. Try a lighter core (e.g. `snes9x` instead of `bsnes`), or accept the stutter.
- **Tab is backgrounded.** Keep the play tab foregrounded as most browsers throttle background tabs.
- **Other tabs eating CPU.** Close them!

## Save states crash on load

- **Core changed between save and load.** States are emulator-build-specific, start fresh or switch to in-game saves (portable across builds).
- **Desktop emulator save state.** States from desktop emulators might not work in-browser.

## DOS games fail to boot

See the [MS-DOS](../using/in-browser-play/ms-dos.md) page for DOS-specific notes.

## Performance on mobile

- **Use Chrome on Android, Safari on iOS.** Other browsers are measurably slower for WASM.
- **Close other tabs.**
- **Try a lighter core.** `snes9x` over `bsnes`, `fceumm` over `nestopia`, etc.
- **Consider a native app.** [Argosy Launcher](../ecosystem/first-party-apps.md#argosy-launcher) on Android uses native emulators, which are orders of magnitude more efficient.

For Netplay-specific issues: [Netplay Troubleshooting](netplay.md).
