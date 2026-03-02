<!-- trunk-ignore-all(markdownlint/MD041) -->

[EmulatorJS](https://emulatorjs.org/) is a web-based emulator for various system; that is, it allows you to run old games in your web browser. It's based on [`RetroArch`](https://www.retroarch.com) compiled with [`Emscripten`](https://emscripten.org/), which is a toolchain for compiling C and C++ code to WebAssembly.

<!-- prettier-ignore -->
!!! warning
    - Emulation is a complex and resource-intensive process. As such, it may not work well in all browser, especially older or less powerful ones. If you're having trouble running a game, try using a different browser or device.
    - PSP emulation with the `ppsspp` core and MS-DOS with the `dosbox-pure` core are not currently supported when using the Console mode.

<!-- prettier-ignore -->
!!! note
    Some platforms may require multiple BIOS/firmware files to be loaded at the same time. To do this, create a **ZIP archive** containing all the firmware files for the emulator you've selected and upload it to the **firmware** section of the platform. This ZIP file will be recognized by EmulatorJS as the firmware bundle for the platform. Refer to the [EmulatorJS documentation](https://emulatorjs.org/docs/systems/) for the required list of files for each platform.

### Saves and states

Our integration with EmulatorJS automates the process of loading and save files and save states. Before starting the game, select a save and/or state file to load (if one is available). Anytime you manually save the game (or create a save state) by clicking the save or "save and quit" buttons, the save and state files stored with RomM will be updated, so there's no need to manually download or upload them.

### Keyboard Lock

Some emulation platforms use the Escape key, which is reserved (by default) in browsers for exiting fullscreen mode.  Some browsers support an additional keyboard lock, where the Escape key can instead be forwarded to the application, and exiting fullscreen mode requires holding the Escape key for a few seconds.  To enable this keyboard lock, set the `emulatorjs.keyboard_lock` option in your `config.yml`:

```yaml
emulatorjs:
  keyboard_lock: true
```

This is not supported by all browsers but is known to work with Chrome.

### Netplay

Netplay lets you play with friends remotely, in realtime with the build-in web player. As it emulates playing on the same console with two controllers while streaming the video to players 2+, it's best for 2-player, co-op, turn based and party games.

Start by enabling netplay in your `config.yml`:

```yaml
emulatorjs:
    netplay:
        enabled: true
```

If you require ICE servers for NAT traversal, we recommend a free-tier [Metered](https://www.metered.ca/stun-turn) account. Create new "TURN Credentials" and replace `<username>` and `<password>` with the entries under "Show ICE Server Array":

```yaml
emulatorjs:
    netplay:
        ice_servers:
            - urls: "stun:stun.relay.metered.ca:80"
            - urls: "stun:stun.relay.metered.ca:80"
            - urls: "turn:global.relay.metered.ca:80"
              username: "<username>"
              credential: "<password>"
            - urls: "turn:global.relay.metered.ca:80?transport=tcp"
              username: "<username>"
              credential: "<password>"
            - urls: "turn:global.relay.metered.ca:443"
              username: "<username>"
              credential: "<password>"
            - urls: "turns:global.relay.metered.ca:443?transport=tcp"
              username: "<username>"
              credential: "<password>"
```

Alternatively, use the free STUN servers from Google and TURN servers via the OpenRelayProject:

```yaml
emulatorjs:
    netplay:
        ice_servers:
            - urls: "stun:stun.l.google.com:19302"
            - urls: "stun:stun1.l.google.com:19302"
            - urls: "stun:stun2.l.google.com:19302"
            - urls: "turn:openrelay.metered.ca:80"
              username: "openrelayproject"
              credential: "openrelayproject"
            - urls: "turn:openrelay.metered.ca:443"
              username: "openrelayproject"
              credential: "openrelayproject"
```

To host a game, start it, then hit the 🌐 icon in botton bar. Set your name, create a room (password optional), and other players should be able to see and join your room. **All players need access to your RomM server to join a room and play together.**

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
