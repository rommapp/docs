---
title: In-Browser Play
description: Play games directly in your browser with EmulatorJS and Ruffle: controls, saves, netplay, fullscreen.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

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
- **During play**: any in-emulator save (SRAM flush) or state creation is written straight back to the storage.
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

## MS-DOS

DOS games run via the `dosbox-pure` core. Create a DOS platform (folder named `dos`) and drop your games in. Operator tuning lives in [Configuration File → `emulatorjs`](../reference/configuration-file.md#emulatorjs) (notably `disable_batch_bootup` for DOS-specific issues).

<!-- prettier-ignore -->
!!! tip "Upload games as `.zip`"
    `dosbox-pure` knows how to unzip and auto-mount zipped DOS games, which is much easier than packaging a raw folder.

<!-- prettier-ignore -->
!!! info "Save states work"
    Once you've got a game running, save state and resume from there, so you only need to do the boot dance once per game.

### Game categories

DOS games come in three flavours, each needing a different approach:

- **Homebrew:** indie / modern DOS games, just an `.exe` that usually Just Works once mounted
- **Shareware demos:** what most "free DOS games" sites distribute, same as homebrew with all files in one folder
- **Retail:** need the original CD mounted alongside the installed game files, which means more work and every game is different

### The manual way (commandline)

Select `Commandline` from the initial loading screen, then:

```text
mount A / -t floppy     # mount the game files
A:                      # switch to that drive
dir                     # find the .EXE
filename.exe            # launch
```

Works for homebrew and shareware. Retail games usually fail here because they want a CD mounted somewhere.

### The automatic way (`.conf` autoload)

`dosbox-pure` looks for a `.conf` file matching the `.exe` name before booting. If found, it reads the config, mounts whatever's specified, and runs the `[autoexec]` block.

Once you have a working `.conf`, click Play → game boots straight into DOS → `[autoexec]` runs → you're in the game, with no typing.

#### Homebrew / demo example: DOOM shareware

1. Confirm no `.ins`, `.cue`, or `.bin` files in the folder (those mean it's a retail CD game).
2. Create `DOOM.conf` next to `DOOM.exe`:

<details>
<summary>DOOM.conf</summary>

```ini
[sdl]
fullscreen=TRUE
fulldouble=false
fullresolution=Fixed
windowresolution=1280x800
output=direct3d
autolock=true

[dosbox]
machine=svga_s3
memsize=16

[render]
frameskip=0
aspect=false
scaler=normal3x

[cpu]
core=auto
cputype=auto
cycles=max

[mixer]
nosound=false
rate=22050
blocksize=2048

[sblaster]
sbtype=sb16
sbbase=220
irq=7
dma=1
oplmode=auto

[speaker]
pcspeaker=true

[joystick]
joysticktype=auto

[dos]
xms=true
ems=true
umb=true

[autoexec]
@echo off
Mount C ".."
C:
cls
DOOM.exe
:exit
exit
```

</details>

Walkthrough of `[autoexec]`:

- `Mount C ".."`: mount the current folder as drive `C:`.
- `C:`: switch to `C:`.
- `cls`: clear the screen.
- `DOOM.exe`: launch the game.
- `:exit` + `exit`: return after quitting.

3. Zip up the folder (including `DOOM.conf`).
4. Upload to RomM under the `dos` platform.
5. Click Play, and the game boots.

Blank screen after boot? Something's off in `[autoexec]`, usually a path or mount issue.

#### Retail with CD example: Dungeon Keeper

Retail games need the game CD image mounted alongside the install directory.

1. Organise files:
    ```text
    DungeonKeeper/
      KEEPER.exe
      KEEPER.cfg
      ...
      CD/
        DUNGEON.CUE
        DUNGEON.BIN
    ```
2. Read `KEEPER.cfg`: it tells you where the game expects the CD.
3. Create `KEEPER.conf` with this `[autoexec]`:

    ```ini
    [autoexec]
    @echo off
    Mount C ".."
    C:
    cd CD
    imgmount d DUNGEO~8.CUE -t iso -fs iso
    cd ..
    cls
    KEEPER.exe
    :exit
    exit
    ```

    Key lines:

    - `Mount C ".."`: game files as `C:`
    - `imgmount d DUNGEO~8.CUE -t iso -fs iso`: CD image as `D:`
    - `cd ..`: back to `C:\` where `KEEPER.exe` lives
    - `KEEPER.exe`: run.

    (File names in DOS are 8.3: `DUNGEON8.CUE` becomes `DUNGEO~8.CUE`.)

4. Zip, upload, play.

<!-- prettier-ignore -->
!!! info "GOG DOS re-releases don't work"
    GOG's DOS games ship with custom wrappers (DOSBox Staging, ScummVM scripts, etc.) that don't translate to `dosbox-pure`: 100% failure rate observed. For GOG titles, extract the underlying game files and build a `.conf` yourself.

#### Retail troubleshooting

If the game lands on a blank DOS prompt:

1. **Remove the final `.exe` line from `[autoexec]`**, which drops you at a prompt after mounting, then check manually:
    - Is the game directory mounted correctly?
    - `type DEFAULT.cfg` (or whatever the game's config is named): the install path should line up with what you mounted.
2. **Check drive paths**: many retail DOS games hard-code `D:\` as the CD, so if you mount the CD as `E:` the game won't find it.
3. **Debug with native `dosbox-pure`**: run the same zip in [RetroArch](https://retroarch.com/) with the `dosbox-pure` core. If it works there it should work in RomM, and if it doesn't the `.conf` is the problem.

### Config file deep dive

The DOOM example is minimal. The full config can include dozens more options (sound card tweaks, CPU cycles, joysticks, IPX networking). The [`dosbox-pure` wiki](https://github.com/schellingb/dosbox-pure) is the authoritative reference for every option.

### Netplay on DOS

Not supported. `dosbox-pure` works with EmulatorJS Netplay intermittently rather than reliably, so stick to single-player for DOS.

### Known issues

- **Mouse lag**: enable `autolock=true` in `[sdl]`.
- **Wrong resolution / aspect**: tweak `[render] aspect=` and `windowresolution=`.
- **Audio crackle**: lower `rate=22050` to `rate=11025` or raise the mixer blocksize.
- **Game runs too fast**: most auto-cycle issues, so set `cycles=fixed 4000` (or another number) explicitly.
- **Keyboard doesn't work for certain keys**: `usescancodes=false` sometimes fixes it.

### Dosemu / Exodos alternatives

Dosemu (Linux native) and Exodos (Windows frontend) are separate DOS tools, not integrated into RomM. If you have an Exodos installation you want to browse through RomM, add the Exodos `MS-DOS/eXoDOS/Games/` folder as a `dos` platform in RomM and RomM will see every game as a normal DOS ROM.

## Ruffle

[Ruffle](https://ruffle.rs/) is a Flash / Shockwave player in WebAssembly. Useful for preserving the Flash game era.

<!-- prettier-ignore -->
!!! important "Ruffle needs the right platform folder"
    Ruffle only plays games from platform folders named `flash` or `browser`. If your Flash games are elsewhere, either rename the folder or add a [platform binding](../reference/configuration-file.md#systemplatforms) in `config.yml`.

No controller mapping, so gamepad-only users will struggle with most Flash titles.

### Saves

Ruffle writes Flash's local-storage to the assets directory. Appears under the game's **Game Data** tab like emulator saves.

### Supported games

Most 2D Flash games work. 3D Shockwave and some advanced ActionScript titles may have rendering glitches. See [Ruffle compatibility](https://ruffle.rs/#compatibility).

### Metadata

If you enable the [Flashpoint](../administration/metadata providers.md#flashpoint) provider, Ruffle games pick up descriptions, cover art, and tags from the Flashpoint database.

## Troubleshooting

- **Game won't boot**: check firmware is uploaded for platforms that need it. `docker logs romm | grep -i emulator` for server-side hints
- **Black screen, no audio**: core is incompatible with your browser. Try a different browser (Chrome / Firefox are most tested) or a different core via in-game Menu → **Core**.
- **Controls do nothing**: browser needs focus. Click once on the emulator canvas. Some cores need a button press to enumerate gamepads.
- **Netplay "failed to start game"**: see [Netplay troubleshooting](../troubleshooting/netplay.md).
- **DOS game fails to autorun**: try [`emulatorjs.disable_batch_bootup: true`](../reference/configuration-file.md#emulatorjs) in `config.yml`.

More in [In-Browser Play Troubleshooting](../troubleshooting/in-browser-play.md).
