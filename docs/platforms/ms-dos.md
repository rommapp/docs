---
title: MS-DOS
description: How to run DOS games in RomM via dosbox-pure, homebrew, shareware demos, and retail CDs.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# MS-DOS

DOS games run in RomM via [`dosbox-pure`](https://github.com/schellingb/dosbox-pure), the EmulatorJS integration: create a DOS platform (folder named `dos`) and drop your games in.

<!-- prettier-ignore -->
!!! tip "Upload games as `.zip`"
    `dosbox-pure` knows how to unzip and auto-mount zipped DOS games, which is much easier than packaging a raw folder.

<!-- prettier-ignore -->
!!! info "Save states work"
    Once you've got a game running, save state and resume from there, so you only need to do the boot dance once per game.

## Game categories

DOS games come in three flavours, each needing a different approach:

- **Homebrew:** indie / modern DOS games, just an `.exe` that usually Just Works once mounted.
- **Shareware demos:** what most "free DOS games" sites distribute, same as homebrew with all files in one folder.
- **Retail:** need the original CD mounted alongside the installed game files, which means more work and every game is different.

## The manual way (commandline)

Select `Commandline` from the initial loading screen, then:

```text
mount A / -t floppy     # mount the game files
A:                      # switch to that drive
dir                     # find the .EXE
filename.exe            # launch
```

Works for homebrew and shareware but retail games usually fail here because they want a CD mounted somewhere.

## The automatic way (`.conf` autoload)

`dosbox-pure` looks for a `.conf` file matching the `.exe` name before booting. If found, it reads the config, mounts whatever's specified, and runs the `[autoexec]` block.

Once you have a working `.conf`, click Play → game boots straight into DOS → `[autoexec]` runs → you're in the game, with no typing.

### Homebrew / demo example: DOOM shareware

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

### Retail with CD example: Dungeon Keeper

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

    - `Mount C ".."`: game files as `C:`.
    - `imgmount d DUNGEO~8.CUE -t iso -fs iso`: CD image as `D:`.
    - `cd ..`: back to `C:\` where `KEEPER.exe` lives.
    - `KEEPER.exe`: run.

    (File names in DOS are 8.3: `DUNGEON8.CUE` becomes `DUNGEO~8.CUE`.)

4. Zip, upload, play.

<!-- prettier-ignore -->
!!! info "GOG DOS re-releases don't work"
    GOG's DOS games ship with custom wrappers (DOSBox Staging, ScummVM scripts, etc.) that don't translate to `dosbox-pure`: 100% failure rate observed. For GOG titles, extract the underlying game files and build a `.conf` yourself.

### Retail troubleshooting

If the game lands on a blank DOS prompt:

1. **Remove the final `.exe` line from `[autoexec]`**, which drops you at a prompt after mounting, then check manually:
    - Is the game directory mounted correctly?
    - `type DEFAULT.cfg` (or whatever the game's config is named): the install path should line up with what you mounted.
2. **Check drive paths**: many retail DOS games hard-code `D:\` as the CD, so if you mount the CD as `E:` the game won't find it.
3. **Debug with native `dosbox-pure`**: run the same zip in [RetroArch](https://retroarch.com/) with the `dosbox-pure` core. If it works there it should work in RomM, and if it doesn't the `.conf` is the problem.

## Config file deep dive

The DOOM example above is minimal: the full config can include dozens more options (sound card tweaks, CPU cycles, joysticks, IPX networking), and the `dosbox-pure` wiki is the authoritative reference for every option.

## Netplay on DOS

Not supported: `dosbox-pure` works with EmulatorJS Netplay intermittently rather than reliably, so stick to single-player for DOS.

## Known issues

- **Mouse lag**: enable `autolock=true` in `[sdl]`.
- **Wrong resolution / aspect**: tweak `[render] aspect=` and `windowresolution=`.
- **Audio crackle**: lower `rate=22050` to `rate=11025` or raise the mixer blocksize.
- **Game runs too fast**: most auto-cycle issues, so set `cycles=fixed 4000` (or another number) explicitly.
- **Keyboard doesn't work for certain keys**: `usescancodes=false` sometimes fixes it.

## Dosemu / Exodos alternatives

Dosemu (Linux native) and Exodos (Windows frontend) are separate DOS tools, not integrated into RomM. If you have an Exodos installation you want to browse through RomM, add the Exodos `MS-DOS/eXoDOS/Games/` folder as a `dos` platform in RomM and RomM will see every game as a normal DOS ROM.

## See also

- [In-Browser Play](../using/in-browser-play.md): general EmulatorJS behaviour.
- [EmulatorJS Configuration](emulatorjs-config.md): operator-level tuning, including `disable_batch_bootup` for DOS-specific issues.
- [dosbox-pure docs](https://github.com/schellingb/dosbox-pure): upstream reference for every config option.
