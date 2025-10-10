<!-- trunk-ignore-all(markdownlint/MD041) -->

[EmulatorJS](https://emulatorjs.org/) is a web-based emulator for various system; that is, it allows you to run old games in your web browser. It's based on [`RetroArch`](https://www.retroarch.com) compiled with [`Emscripten`](https://emscripten.org/), which is a toolchain for compiling C and C++ code to WebAssembly.

<!-- prettier-ignore -->
!!! warning
    - Emulation is a complex and resource-intensive process. As such, it may not work well in all browser, especially older or less powerful ones. If you're having trouble running a game, try using a different browser or device.
    - PSP emulation with the `ppsspp` core and MS-DOS with the `dosbox-pure` core are not currently supported when using the Console mode.

<!-- prettier-ignore -->
!!! note
    Some platforms may require multiple BIOS/firmware files to be loaded at the same time. To do this, create a **ZIP archive** containing all the firmware files for the emulator you've selected and upload it to the **firmware** section of the platform. This ZIP file will be recognized by EmulatorJS as the firmware bundle for the platform. Refer to the [EmulatorJS documentation](https://emulatorjs.org/docs/systems/) for the required list of files for each platform.

### Loading saves and states

Our integration with EmulatorJS automates the process of loading and save files and save states. Before starting the game, select a save and/or state file to load (if one is available). Anytime you manually save the game (or create a save state) by clicking the save or "save and quit" buttons, the save and state files stored with RomM will be updated, so there's no need to manually download or upload them.

### Supported systems

Note that only the following systems are currently supported:

- 3DO
- Amiga
- Arcade/MAME
- Atari 2600
- Atari 5200
- Atari 7800
- Atari Jaguar
- Atari Lynx
- Commodore 64
- ColecoVision
- DOOM
- Neo Geo Pocket
- Neo Geo Pocket Color
- MS-DOS
- Nintendo 64
- Nintendo Entertainment System (NES)
- Nintendo Family Computer (Famicom)
- Nintendo DS
- Game Boy
- Game Boy Color
- Game Boy Advance
- PC-FX
- PlayStation (PS)
- PlayStation Portable (PSP)
- Sega 32X
- Sega CD
- Sega Game Gear
- Sega Master System
- Sega Genesis/Megadrive
- Sega Saturn
- Super Nintendo Entertainment System (SNES)
- Super Famicom
- TurboGraphx-16/PC Engine
- Virtual Boy
- WonderSwan
- WonderSwan Color
