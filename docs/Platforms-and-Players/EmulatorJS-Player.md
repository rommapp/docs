<!-- trunk-ignore-all(markdownlint/MD041) -->

[EmulatorJS](https://emulatorjs.org/) is a web-based emulator for various system; that is, it allows you to run old games in your web browser. It's based on [`RetroArch`](https://www.retroarch.com) compiled with [`Emscripten`](https://emscripten.org/), which is a toolchain for compiling C and C++ code to WebAssembly.

<!-- prettier-ignore -->
!!! warning
    Due to a [change by Apple in iOS 18.2](https://bugs.webkit.org/show_bug.cgi?id=284752), emulation is severely limited, and likely non-functional, on iOS 18.2-18.3 devices. This was fixed in iOS 18.4

<!-- prettier-ignore -->
!!! warning
    PSP emulation with the PPSSPP core and MS-DOS with the dosbox-pure core requires one of the three options:

    - the unofficial [desktop app](https://github.com/smurflabs/RommBrowser/releases) published by [smurflabs](https://github.com/smurflabs). Once logged into the app, you can enable the required settings under `Developer Settings`. (Preferred)
    - [special setup with a reverse proxy](https://emulatorjs.org/docs/options#ejs_threads) - If you use this you will be **MISSING** features within RomM and it is recommended to use the WebApp
    - launching Chrome browser with the `--disable-web-security` and `--enable-features=SharedArrayBuffer` flags, which **WE STRONGLY DISCOURAGE** as it disables important security features.

<!-- prettier-ignore -->
!!! warning
    Emulation is a complex and resource-intensive process. As such, it may not work well in all browser, especially older or less powerful ones. If you're having trouble running a game, try using a different browser or device.

### Loading saves and states

Our integration with EmulatorJS automates the process of loading and saving save files and save states. Before starting the game, select a save and/or state file to load (if one is available). Anytime you save the game (or create a save state), the save and state files stored with RomM will be updated, so there's no need to manually download or upload them.

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
