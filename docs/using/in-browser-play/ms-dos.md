---
title: MS-DOS
description: Run DOS games in the browser via dosbox-pure
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# MS-DOS

DOS games run via the `dosbox-pure` core (part of [EmulatorJS](emulatorjs.md)). Create a DOS platform (folder named `dos`) and drop your games in. Operator tuning lives in [Configuration File → `emulatorjs`](../../reference/configuration-file.md#emulatorjs) (notably `disable_batch_bootup` for DOS-specific issues).

<!-- prettier-ignore -->
!!! tip "Upload games as `.zip`"
    `dosbox-pure` knows how to unzip and auto-mount zipped DOS games, which is much easier than packaging a raw folder.

<!-- prettier-ignore -->
!!! info "Save states work"
    Once you've got a game running, save state and resume from there, so you only need to do the boot dance once per game.

## Running games

DOS games come in three flavours, each needing a different approach:

- **Homebrew:** indie/modern DOS games, just an `.exe` that usually Just Works once mounted.
- **Shareware demos:** what most "free DOS games" sites distribute, same as homebrew with all files in one folder.
- **Retail:** need the original CD mounted alongside the installed game files. More work, and every game is different.

The basic flow inside `dosbox-pure`: select `Commandline` from the initial loading screen, then:

```text
mount A/-t floppy     # mount the game files
A:                      # switch to that drive
dir                     # find the .EXE
filename.exe            # launch
```

Works for homebrew and shareware, but retail games usually fail here because they want a CD mounted somewhere.

## Auto-config with `.conf` files

<!-- prettier-ignore -->
!!! warning "Not for the faint of heart"
    Building working `.conf` files is trial-and-error, so plan for it.

`dosbox-pure` looks for a `.conf` file matching the `.exe` name before booting. If found, it reads the config, mounts whatever's specified, and runs the `[autoexec]` block. Once you have a working `.conf`, click Play → game boots straight into DOS → `[autoexec]` runs → you're in the game, no typing.

### DOOM shareware example

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
sensitivity=100
waitonerror=true
priority=higher,normal
mapperfile=mapper-0.74.map
usescancodes=true

[dosbox]
machine=svga_s3
captures=.\Captures\
memsize=16

[render]
frameskip=0
aspect=false
scaler=normal3x

[cpu]
core=auto
cputype=auto
cycles=max
cycleup=10
cycledown=20

[mixer]
nosound=false
rate=22050
blocksize=2048
prebuffer=10

[midi]
mpu401=intelligent
mididevice=default
midiconfig=

[sblaster]
sbtype=sb16
sbbase=220
irq=7
dma=1
hdma=5
sbmixer=true
oplmode=auto
oplemu=default
oplrate=44100

[gus]
gus=false
gusrate=44100
gusbase=240
gusirq=5
gusdma=3
ultradir=C:\ULTRASND

[speaker]
pcspeaker=true
pcrate=44100
tandy=auto
tandyrate=44100
disney=true

[joystick]
joysticktype=fcs
timed=true
autofire=false
swap34=false
buttonwrap=false

[serial]
serial1=dummy
serial2=dummy
serial3=disabled
serial4=disabled

[dos]
xms=true
ems=true
umb=true
keyboardlayout=auto

[ipx]
ipx=false

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

The `[autoexec]` block does the work: mount the current folder as `C:`, switch to it, clear the screen, run `DOOM.exe`, then drop back to the prompt on quit.

3. Zip up the folder (including `DOOM.conf`).
4. Upload under the `dos` platform.
5. Click Play, and the game boots.

A blank screen after boot usually points at a path or mount issue in `[autoexec]` (see [Troubleshooting](#troubleshooting) below).

## Retail games with CDs

Retail games need the game CD image mounted alongside the install directory.

<!-- prettier-ignore -->
!!! info "GOG DOS re-releases don't work"
    GOG's DOS games ship with custom wrappers (DOSBox Staging, ScummVM scripts, etc.) that don't translate to `dosbox-pure`, with a 100% failure rate observed. For GOG titles, extract the underlying game files and build a `.conf` yourself.

### Dungeon Keeper Gold example

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

2. Read `KEEPER.cfg`, which tells you where the game expects the CD.
3. Create `KEEPER.conf` matching the `.exe` name:

<details>
<summary>KEEPER.conf</summary>

```ini
[sdl]
fullscreen=TRUE
fulldouble=false
fullresolution=Fixed
windowresolution=1280x800
output=direct3d
autolock=true
sensitivity=100
waitonerror=true
priority=higher,normal
mapperfile=mapper-0.74.map
usescancodes=true

[dosbox]
machine=svga_s3
captures=.\Captures\
memsize=16

[render]
frameskip=0
aspect=false
scaler=normal3x

[cpu]
core=auto
cputype=auto
cycles=max
cycleup=10
cycledown=20

[mixer]
nosound=false
rate=22050
blocksize=2048
prebuffer=10

[midi]
mpu401=intelligent
mididevice=default
midiconfig=

[sblaster]
sbtype=sb16
sbbase=220
irq=7
dma=1
hdma=5
sbmixer=true
oplmode=auto
oplemu=default
oplrate=44100

[gus]
gus=false
gusrate=44100
gusbase=240
gusirq=5
gusdma=3
ultradir=C:\ULTRASND

[speaker]
pcspeaker=true
pcrate=44100
tandy=auto
tandyrate=44100
disney=true

[joystick]
joysticktype=fcs
timed=true
autofire=false
swap34=false
buttonwrap=false

[serial]
serial1=dummy
serial2=dummy
serial3=disabled
serial4=disabled

[dos]
xms=true
ems=true
umb=true
keyboardlayout=auto

[ipx]
ipx=false

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

</details>

Key `[autoexec]` lines for retail:

- `Mount C ".."`: game files as `C:`.
- `imgmount d DUNGEO~8.CUE -t iso -fs iso`: CD image as `D:`.
- `cd ..`: back to `C:\` where `KEEPER.exe` lives.
- `KEEPER.exe`: run.

(File names in DOS are 8.3, so `DUNGEON8.CUE` becomes `DUNGEO~8.CUE`.)

4. Zip, upload, play.

## Troubleshooting

If a game lands on a blank DOS prompt or won't boot:

1. **Strip the `[autoexec]` `.exe` line** so `dosbox-pure` drops you at a prompt after mounting. Then check manually:
    - Is the game directory mounted correctly?
    - `type DEFAULT.cfg` (or whatever the game's config is named): the install path should match what you mounted.
2. **Check drive paths**. Many retail DOS games hard-code `D:\` as the CD. If you mount the CD as `E:` the game won't find it.
3. **Debug with native `dosbox-pure`**. Run the same zip in [RetroArch](https://retroarch.com/) with the `dosbox-pure` core. If it works there it should work, and if not, the `.conf` is the problem.

Full option reference available at [`dosbox-pure` wiki](https://github.com/schellingb/dosbox-pure).
