---
title: In-Browser Play
description: Play games directly in your browser with EmulatorJS and Ruffle: controls, saves, netplay, fullscreen.
---

# In-Browser Play

RomM ships with two in-browser emulators:

- **EmulatorJS**: RetroArch cores compiled to WebAssembly. Covers NES, SNES, Genesis, N64, PSX, PSP, Saturn, and 30+ other platforms.
- **Ruffle**: Flash / Shockwave emulator for browser games

Hit the **Play** button on any supported game, and the emulator loads full-screen in a new page. Same UI on desktop, mobile, and Console Mode.

## EmulatorJS

[EmulatorJS](https://emulatorjs.org/) is a web-based emulator running [RetroArch](https://www.retroarch.com) via [Emscripten](https://emscripten.org/), so cores you know from RetroArch show up here.

<!-- prettier-ignore -->
!!! warning "Emulation is resource-intensive"
    Older or less-powerful devices may struggle, especially with demanding cores (Dreamcast, Saturn, PSP). Try a different browser or device before filing a bug.

<!-- prettier-ignore -->
!!! note "Some cores don't work in Console Mode"
    PSP (`ppsspp`) and MS-DOS (`dosbox-pure`) aren't supported in [Console Mode](console-mode.md). Use the main UI for those.

### Supported platforms

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

Full up-to-date list: [EmulatorJS Systems docs](https://emulatorjs.org/docs/systems/).

### Firmware

Some platforms need BIOS / firmware: PlayStation, Saturn, Sega CD, PSP, DS. Upload via [Firmware Management](../administration/firmware-management.md) or by dropping files in the right `bios/` folder and rescanning.

<!-- prettier-ignore -->
!!! note "Zip bundles for multi-file firmware"
    Some cores need several BIOS files. Create a **zip archive** containing all of them and upload that zip through the Firmware tab on the platform detail page. EmulatorJS picks it up as a single firmware bundle. See [EmulatorJS Systems docs](https://emulatorjs.org/docs/systems/) for the per-platform file list.

### Launching a game

Three paths:

1. **Game card hover** → **Play** icon.
2. **Game detail page** → **Play** button.
3. **Console Mode** → select game → **A** button.

If the platform doesn't support in-browser play, Play is replaced with Download.

### Controls

EmulatorJS maps keyboard and gamepad automatically. Defaults are core-specific but approximate the original console layout. Rebind in-game via the **Menu** button during play.

Operator-level default overrides live in `config.yml`. See [Configuration File → `emulatorjs.controls`](../reference/configuration-file.md#emulatorjscontrols).

Keyboard + gamepad can be used simultaneously for multi-player: player 2 on the gamepad, player 1 on the keyboard, for example.

### Saves and states

RomM integrates with EmulatorJS so save-files and save-states are loaded and saved automatically:

- **Before launch**: if multiple saves exist, RomM asks which to load.
- **During play**: any in-emulator save (SRAM flush) or state creation is written straight back to RomM's storage.
- **After quit**: everything is already persisted. No manual download

Full details: [Saves & States](saves-and-states.md).

### Cheats

In-game Menu → **Cheats** → add manually or load a list. Saved cheats persist per-user per-ROM. RomM doesn't ship a cheat database, so you bring your own codes.

### Screenshots

During play: in-game Menu → **Screenshot**. Saved to your personal screenshot collection for the ROM. Appears on the Screenshots tab of the game detail page.

### Fullscreen

- **F11**: browser fullscreen
- In-game Menu → **Fullscreen** button: same thing

### Multi-disc games

RomM asks which disc to boot before launching. During play, in-game Menu → **Switch Disc** → pick another disc without exiting (works for cores that support runtime disc swap: PSX, Saturn).

### Cache / unload behaviour

Operators can tune how aggressively the emulator caches and unloads via [`emulatorjs.cache_limit` and `emulatorjs.disable_auto_unload`](../reference/configuration-file.md#emulatorjs) in `config.yml`. Defaults are fine for normal use.

### Full-screen on play

Profile → User Interface → **Fullscreen on launch**: always enters fullscreen when you hit Play. Handy on TVs.

### Per-core settings

In-game Menu → **Settings**: core-specific knobs (vsync, region, sound quality). Your tweaks persist per-core per-user but operator defaults in [`config.yml`](../reference/configuration-file.md#emulatorjssettings) set the initial values.

### Netplay

See [Netplay](netplay.md). One-page deep dive on hosting/joining, ICE servers, and NAT tradeoffs.

## Ruffle

[Ruffle](https://ruffle.rs/) is a Flash / Shockwave player in WebAssembly. Useful for preserving the Flash game era.

<!-- prettier-ignore -->
!!! important "Ruffle needs the right platform folder"
    Ruffle only plays games from platform folders named `flash` or `browser`. If your Flash games are elsewhere, either rename the folder or add a [platform binding](../reference/configuration-file.md#systemplatforms) in `config.yml`.

No controller mapping, so gamepad-only users will struggle with most Flash titles.

### Saves

Ruffle writes Flash's local-storage to RomM's assets directory. Appears under the game's **Game Data** tab like emulator saves.

### Supported games

Most 2D Flash games work. 3D Shockwave and some advanced ActionScript titles may have rendering glitches. See [Ruffle compatibility](https://ruffle.rs/#compatibility).

### Metadata

If you enable the [Flashpoint](../administration/metadata-providers.md#flashpoint) provider, Ruffle games pick up descriptions, cover art, and tags from the Flashpoint database.

## Troubleshooting

- **Game won't boot**: check firmware is uploaded for platforms that need it. `docker logs romm | grep -i emulator` for server-side hints
- **Black screen, no audio**: core is incompatible with your browser. Try a different browser (Chrome / Firefox are most tested) or a different core via in-game Menu → **Core**.
- **Controls do nothing**: browser needs focus. Click once on the emulator canvas. Some cores need a button press to enumerate gamepads.
- **Netplay "failed to start game"**: see [Netplay troubleshooting](../troubleshooting/netplay.md).
- **DOS game fails to autorun**: try [`emulatorjs.disable_batch_bootup: true`](../reference/configuration-file.md#emulatorjs) in `config.yml`.

More in [In-Browser Play Troubleshooting](../troubleshooting/in-browser-play.md).
