---
title: EmulatorJS
description: Play retro games in your browser
---

# EmulatorJS

[EmulatorJS](https://emulatorjs.org/) is the in-browser retro emulator that powers RomM's **Play** button. It runs [RetroArch](https://www.retroarch.com) cores compiled to WebAssembly via [Emscripten](https://emscripten.org/). Hit Play on any supported game and the emulator loads full-screen in a new page.

<!-- prettier-ignore -->
!!! warning "Emulation is resource-intensive"
    Older or less-powerful devices may struggle, especially with demanding cores (Dreamcast, Saturn, PSP). Try a different browser or device before filing a bug.

<!-- prettier-ignore -->
!!! note "Some cores don't work in Console Mode"
    PSP (`ppsspp`) and MS-DOS (`dosbox-pure`) aren't supported in [Console Mode](../console-mode.md).

<!-- prettier-ignore -->
!!! note "Zip bundles for multi-file firmware"
    Some cores need several BIOS files. Bundle them into a **zip archive** and upload via the Firmware tab on the platform detail page, and EmulatorJS picks it up as a single firmware bundle (see [Firmware Management](../../administration/firmware-management.md)).

## Saves and states

RomM's EmulatorJS integration automates save-file and save-state handling: if a save or state already exists you're prompted to pick one before launch, and any in-emulator save or state is written straight back to the server with no manual download or re-upload step. Full details in [Saves & States](../saves-and-states.md).

## Netplay

Available in 5.0+. Up to four players can join a room hosted on your instance, with inputs streamed to the host over WebRTC, best for co-op and turn-based games (frame-perfect fighting isn't realistic over the internet).

Operator setup (ICE servers, enable flag) lives in [Configuration File → `emulatorjs.netplay`](../../reference/configuration-file.md#emulatorjsnetplay-new-in-50). End-user docs live in [Netplay](../netplay.md).

<!-- prettier-ignore -->
!!! note "Nightly CDN caveat"
    Enabling Netplay switches some EmulatorJS assets to the nightly CDN. Occasional 404s or untranslated UI strings can show up, but usually self-heal on the next image update.

## Supported systems

| Platform                                            | Cores                                                                    |
| --------------------------------------------------- | ------------------------------------------------------------------------ |
| 3DO                                                 | `opera`                                                                  |
| Amiga                                               | `puae`                                                                   |
| Arcade / MAME                                       | `mame2003_plus`, `mame2003`, `fbneo`                                     |
| Atari 2600 / 5200 / 7800 / Jaguar / Lynx            | Various: `stella2014`, `atari800`, `prosystem`, `virtualjaguar`, `handy` |
| Commodore 64                                        | `vice_x64sc`                                                             |
| ColecoVision                                        | `gearcoleco`                                                             |
| DOOM                                                | `prboom`                                                                 |
| Game Boy / Color / Advance                          | `gambatte`, `mgba`                                                       |
| MS-DOS                                              | `dosbox-pure`                                                            |
| Neo Geo Pocket / Color                              | `mednafen_ngp`                                                           |
| Nintendo DS                                         | `melonds`, `desmume`                                                     |
| Nintendo 64                                         | `mupen64plus_next`, `parallel_n64`                                       |
| NES / Famicom                                       | `fceumm`, `nestopia`                                                     |
| PC-FX                                               | `mednafen_pcfx`                                                          |
| PlayStation                                         | `mednafen_psx_hw`, `pcsx_rearmed`                                        |
| PSP                                                 | `ppsspp`                                                                 |
| Sega 32X / CD / Game Gear / Master System / Genesis | `picodrive`, `genesis_plus_gx`                                           |
| Sega Saturn                                         | `mednafen_saturn`, `yabause`                                             |
| SNES / Super Famicom                                | `snes9x`, `bsnes`                                                        |
| TurboGraphx-16 / PC Engine                          | `mednafen_pce`                                                           |
| Virtual Boy                                         | `mednafen_vb`                                                            |
| WonderSwan / Color                                  | `mednafen_wswan`                                                         |

Player UI features beyond the basics (cheats, in-emulator screenshots, multi-disc swap, hotkeys, fullscreen) are covered in the broader [EmulatorJS docs](https://emulatorjs.org/docs/).
