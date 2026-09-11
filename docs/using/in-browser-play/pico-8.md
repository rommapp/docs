---
title: PICO-8
description: Play PICO-8 cartridges in the browser via FAKE-08
---

# PICO-8

[PICO-8](https://www.lexaloffle.com/pico-8.php) cartridges run in the browser on [FAKE-08](https://github.com/jtothebell/fake-08), an open-source reimplementation of the PICO-8 runtime built to WebAssembly. It's its own player, not a libretro core, so [EmulatorJS](emulatorjs.md) isn't involved.

Put carts under the `pico` platform, either as `.p8` (plain text) or `.p8.png` (PNG-wrapped).

<!-- prettier-ignore -->
!!! info "Full image only"
    FAKE-08 is bundled in the full container image and has **no CDN fallback**, so PICO-8 does not play on the slim image (see [Image Variants](../../install/image-variants.md)).

Operators can turn the player off with `DISABLE_PICO8=true` (see [Environment Variables](../../reference/environment-variables.md)).

## Cartridge art

A `.p8.png` cart is a real PNG, and the image it draws is the cartridge label. RomM just uses the file itself as the cover, so these come out of a scan with their own art and never need a metadata provider for it. Plain `.p8` carts are text with no image in them at all, and fall back to the usual artwork sources.

## Controls

PICO-8 only has a d-pad and two buttons, which every input method maps onto:

| Input        | Mapping                                        |
| ------------ | ---------------------------------------------- |
| **Keyboard** | Arrow keys, `Z` for ❎, `X` for 🅾️             |
| **Gamepad**  | D-pad, plus the A and B face buttons           |
| **Touch**    | On-screen d-pad and buttons                    |
| **Mouse**    | Passed through for carts that read the pointer |

Output is PICO-8's native 128×128 at 30fps, scaled to fit the window. Audio and fullscreen both work.

## How it is bundled

FAKE-08 doesn't publish a web build of its own, so RomM pulls the WebAssembly build out of [p3a](https://github.com/fabkury/p3a). It's pinned to a specific commit and checksummed when the image is built, same as EmulatorJS, Ruffle and `js-dos`. Nothing is downloaded at runtime. Whichever image tag you're running decides the version you get.

## Saves

Cart data doesn't sync back to RomM. Whatever the cartridge saves stays in your browser.

## Related

- [EmulatorJS](emulatorjs.md): the libretro-core player behind most platforms
- [`js-dos`](js-dos.md): the other native, non-EmulatorJS player
- [Image Variants](../../install/image-variants.md): which runtimes each image carries
