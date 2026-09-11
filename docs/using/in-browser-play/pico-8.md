---
title: PICO-8
description: Play PICO-8 cartridges in the browser via FAKE-08
---

# PICO-8

[PICO-8](https://www.lexaloffle.com/pico-8.php) cartridges play in the browser on [FAKE-08](https://github.com/jtothebell/fake-08), an open-source reimplementation of the PICO-8 runtime compiled to WebAssembly. It is a native player rather than a libretro core, so it does not go through [EmulatorJS](emulatorjs.md).

Cartridges go under the `pico` platform, as `.p8` (the plain-text cart format) or `.p8.png` (the PNG-wrapped one).

<!-- prettier-ignore -->
!!! info "Full image only"
    FAKE-08 is bundled in the full container image and has **no CDN fallback**, so PICO-8 does not play on the slim image (see [Image Variants](../../install/image-variants.md)).

Operators can turn the player off with `DISABLE_PICO8=true` (see [Environment Variables](../../reference/environment-variables.md)).

## Cartridge art

A `.p8.png` cartridge **is** a PNG, and what it draws is the cartridge label. RomM uses the file itself as the game's cover, so a PNG cart comes out of a scan with its own art and needs no metadata provider to supply one. Plain `.p8` carts are text and carry no image, so they fall back to the normal artwork sources.

## Controls

PICO-8's whole input model is a d-pad and two buttons, and all four input methods map onto it:

| Input        | Mapping                                              |
| ------------ | ---------------------------------------------------- |
| **Keyboard** | Arrow keys, <kbd>Z</kbd> for ❎, <kbd>X</kbd> for 🅾️ |
| **Gamepad**  | D-pad, plus the A and B face buttons                 |
| **Touch**    | On-screen d-pad and buttons                          |
| **Mouse**    | Passed through for carts that read the pointer       |

The display is PICO-8's native 128×128 at 30 frames per second, scaled to fit, with audio and fullscreen.

## How it is bundled

FAKE-08 itself publishes no web build, so RomM takes the WebAssembly build from [p3a](https://github.com/fabkury/p3a), pinned to a commit and checksummed at image build time, the same way the EmulatorJS, Ruffle and `js-dos` runtimes are. Nothing is fetched at runtime, and the version you get is fixed by the image tag you run.

## Saves

Cart data is not synced back to RomM. Progress persists only as far as the cartridge itself manages it inside the browser.

## Related

- [EmulatorJS](emulatorjs.md): the libretro-core player behind most platforms
- [`js-dos`](js-dos.md): the other native, non-EmulatorJS player
- [Image Variants](../../install/image-variants.md): which runtimes each image carries
