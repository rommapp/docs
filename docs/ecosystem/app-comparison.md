---
title: App Feature Comparison
description: Which first-party and community apps support save sync, playtime tracking, downloads and more
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# App Feature Comparison

This page compares the apps listed in the [RomM README](https://github.com/rommapp/romm#official-apps), so you can see which ones sync saves, track playtime or download games to your device before installing anything. The team builds the first-party apps; community members build and maintain the rest, and the team doesn't review their code.

!!! info "Checked in September 2026"

    Every entry was checked against the app's source code at the version shown in [At a Glance](#at-a-glance). These apps ship updates often, so a feature marked missing here may have landed since. Check the app's own docs before relying on it.

**Legend:** ✅ yes, ⚠️ partly (see the notes), ❌ no, ➖ doesn't apply.

## At a Glance

| App                                                                          | Made by   | Runs on                                              | Checked version |
| ---------------------------------------------------------------------------- | --------- | ---------------------------------------------------- | --------------- |
| [Argosy](first-party-apps.md#argosy-launcher)                                | RomM team | Android 8.0+ handhelds, phones and TVs               | v2.18.0         |
| [Grout](first-party-apps.md#grout)                                           | RomM team | Linux handheld custom firmwares (13 supported)       | v5.3.1.1        |
| [Playnite plugin](first-party-apps.md#playnite-plugin)                       | RomM team | Windows, inside [Playnite](https://playnite.link)    | 0.9.0           |
| [Tender](https://github.com/danielcopper/romm-tender) (formerly DeckyRommSync) | Community | Steam Deck and other SteamOS/Linux PCs, with RetroDECK | 0.33.0          |
| [RetroArch Sync](https://github.com/Covin90/romm-retroarch-sync)             | Community | Linux desktop, including SteamOS                     | v1.6            |
| [SwitchRomM](https://github.com/Shalasere/SwitchRomM)                        | Community | Nintendo Switch (homebrew)                           | v0.2.8          |

Three more community projects in the README aren't game clients. They're covered in [Other Community Tools](#other-community-tools).

## Library and Downloads

| App             | Sign-in                          | Collections                               | Download to device                                    | BIOS | Launches games                                    | Plays offline                        |
| --------------- | -------------------------------- | ----------------------------------------- | ----------------------------------------------------- | ---- | ------------------------------------------------- | ------------------------------------ |
| Argosy          | QR pairing, pairing code         | ✅ Regular (two-way), smart and virtual   | ✅ Queue, multi-disc, extraction, push from RomM 5.4+ | ✅   | ✅ Built-in emulator, RetroArch, ~65 standalone   | ✅                                   |
| Grout           | QR pairing, pairing code         | ✅ Regular, smart and virtual             | ✅ Batch, box art, multi-disc                         | ✅   | ❌ The firmware's own frontend launches them      | ⚠️ Games play, Grout needs the server |
| Playnite plugin | Password, API token, QR pairing  | ❌ Favorites only                         | ✅ Queue, auto-extract                                | ❌   | ✅ Any emulator set up in Playnite                | ✅                                   |
| Tender          | Password, API token, pairing code | ✅ Regular, smart, virtual and favorites | ✅ Queue, multi-disc                                  | ✅   | ✅ RetroDECK (RetroArch and standalone)           | ✅                                   |
| RetroArch Sync  | Pairing code, password           | ✅ Collection Sync downloads them         | ✅ Bulk, multi-disc                                   | ✅   | ✅ RetroArch or RetroDECK                         | ✅                                   |
| SwitchRomM      | Password                         | ❌                                        | ⚠️ Downloads only; install with DBI or similar        | ❌   | ❌                                                | ➖                                   |

Sign-in methods:

- **QR pairing** shows a QR code on the device that you approve in the RomM web UI. It needs RomM 5.0 or later.
- **Pairing code** is the 8-character code from **Client API Tokens → Pair** in RomM, typed into the app (see [Device Pairing](../developers/client-api-tokens.md#device-pairing)).
- **API token** means pasting a full `rmm_` [Client API Token](../developers/client-api-tokens.md). It's the usual route for OIDC-only accounts.
- **Password** means your RomM username and password. Tender uses it once to create a token and then discards it; the Playnite plugin stores it in plain text.

## Sync and Tracking

| App             | Save sync                                                         | State sync                      | Playtime to RomM          | RetroAchievements   | Writes back to RomM                                              |
| --------------- | ----------------------------------------------------------------- | ------------------------------- | ------------------------- | ------------------- | ---------------------------------------------------------------- |
| Argosy          | ✅ Automatic, two-way, [most emulators](#argosy)                  | ✅ [Some emulators](#argosy)    | ✅ Sends and pulls        | ✅ Shows progress   | Ratings, status, favorites, collections, screenshots             |
| Grout           | ⚠️ Manual, two-way, [coverage varies by firmware](#grout)          | ❌                              | ❌                        | ❌                  | Saves only                                                       |
| Playnite plugin | ⚠️ Opt-in, [RetroArch only](#playnite-plugin)                      | ❌                              | ❌ Tracked in Playnite    | ❌ Link only        | Favorites and completion status (opt-in)                         |
| Tender          | ✅ Opt-in, automatic, [RetroArch cores](#tender)                  | ❌ Not planned                  | ✅ Sends and pulls        | ✅ Shows progress   | Saves and play sessions                                          |
| RetroArch Sync  | ✅ Automatic, two-way, [any RetroArch core](#retroarch-sync)      | ✅ Automatic, two-way           | ❌                        | ❌                  | Saves, states and screenshots                                    |
| SwitchRomM      | ❌                                                                | ❌                              | ❌                        | ❌                  | Nothing                                                          |

"Playtime to RomM" means the app posts play sessions to RomM, so they count toward the game's playtime there. "Pulls" means it also reads sessions from your other devices. Apps that sync through RomM's [device sync protocol](../developers/device-sync-protocol.md) (Argosy, Grout, Tender, RetroArch Sync, and the Playnite plugin with save sync on) show up as registered devices in RomM.

## Save Sync by System

Save sync is almost never all-or-nothing: each app knows where some emulators keep their saves and not others. This section lists what each app covers.

### Argosy

Argosy syncs saves before a game launches (when the server copy is newer), when a session ends, every six hours in the background, and on demand from the **Save Sync** screen. Changes made offline upload when you reconnect. Real conflicts ask you to keep the local or the server copy.

| Emulator                                                             | Systems              | Saves | States |
| -------------------------------------------------------------------- | -------------------- | ----- | ------ |
| Built-in emulator                                                    | All 54 built-in cores | ✅    | ✅ Not PSP, CD-i or 3DS |
| RetroArch                                                            | About 70 systems     | ✅    | ✅     |
| PPSSPP (all builds)                                                  | PSP                  | ✅    | ✅     |
| DraStic, melonDS, MelonDualDS                                        | DS                   | ✅    | ✅     |
| SeedlessDS                                                           | DS                   | ✅    | ❌     |
| Pizza Boy (all builds)                                               | GB, GBC, GBA         | ✅    | ✅     |
| Mupen64Plus FZ (all builds)                                          | N64                  | ✅    | ❌     |
| Dolphin family                                                       | GameCube, Wii        | ✅ GameCube needs GCI folder mode | ❌ |
| Cemu                                                                 | Wii U                | ✅    | ❌     |
| Citra, Citra MMJ, Lime3DS, Azahar, Borked3DS                         | 3DS                  | ✅    | ❌     |
| Yuzu, Ryujinx, Eden, Citron, Strato, Skyline, Sudachi, Kenji-NX      | Switch               | ✅    | ❌     |
| NetherSX2, AetherSX2, PCSX2, ARMSX2                                  | PS2                  | ⚠️ Folder memory cards only | ❌ |
| Vita3K                                                               | PS Vita              | ✅    | ❌     |
| MD.emu                                                               | Sega 8/16-bit, Sega CD, 32X | ✅ | ❌ |
| aPS3e, XenDroid, hakuX                                               | PS3, Xbox 360, Xbox  | ⚠️ Experimental | ❌ |
| DuckStation                                                          | PS1                  | ❌ Disabled, Android file permissions | ⚠️ Enabled, may hit the same problem |
| Redream, Flycast, Saturn.emu, Yaba Sanshiro, MAME4droid, FBA, ScummVM, DOSBox apps, AX360E | Various | ❌ | ❌ |

Dreamcast saves only sync through the built-in emulator. Argosy needs **All Files Access** to read emulator save folders; on Android 11 and later, if it can't reach an emulator's folder under `Android/data`, set a custom save path for that emulator.

### Grout

Grout syncs saves both ways when you run **Sync Now** from its sync menu or change a save slot. It doesn't sync in the background or while you play. Conflicts ask you to skip, keep the local copy or keep the server copy, and Grout backs up a local save before overwriting it.

It only picks up files with these extensions: `.srm`, `.sav`, `.dsv`, `.mcr`, `.mcd`, `.brm`, `.eep`, `.sra`, `.fla`, `.mpk` and `.nv`. PSP save folders sync as a zip, matched by game ID. Save states never sync. Which systems sync depends on the firmware:

| Firmware                           | Save sync coverage                                                                                                    |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| muOS                               | ✅ Every platform Grout maps, including many standalone emulators and DraStic                                         |
| Knulli, Batocera, NextUI, MinUI    | ✅ Every platform Grout maps                                                                                          |
| ROCKNIX, ArkOS/dArkOS              | ⚠️ Only emulators that save next to the ROM (for RetroArch, "saves in content directory")                              |
| Anbernic Stock OS                  | ⚠️ RetroArch only; standalone PPSSPP, DraStic and OpenBOR saves don't sync                                             |
| spruce (also sprigUI, twigUI)      | ⚠️ No NDS, PS2, Saturn, OpenBOR or ScummVM                                                                             |
| Allium                             | ⚠️ No PSP, PS2 or OpenBOR                                                                                      |
| Onion, Koriki                      | ⚠️ No PSP, PS2, OpenBOR, CPS1–3, Ports, ScummVM, Satellaview, Super Game Boy, Sufami Turbo or Videopac         |
| TrimUI Stock OS                    | ⚠️ Only arcade, Dreamcast, GB, GBC, GBA, PS1, PSP, Saturn and Super Famicom; no NES, SNES, Genesis, N64 or NDS         |

On Onion, Koriki and Anbernic Stock OS, Grout's install guides ask you to set the device clock before save sync will work. Grout's [platform docs](https://grout.romm.app/) cover each firmware in more detail.

### Playnite Plugin

Save sync is off by default; turn it on in the plugin settings. It then syncs before a game launches (giving up after 20 seconds so the game still starts), after you quit, and from a manual menu item. The newer copy wins a conflict without asking.

Only **RetroArch** is supported, and only its `.srm` save files: companion files like `.rtc` don't sync, and nor do saves from any other emulator. The plugin reads `retroarch.cfg` to find the save folder, including per-core and per-content folder settings.

### Tender

Tender (formerly DeckyRommSync) syncs saves before launch and after exit once save sync is on, and from **Sync All Saves Now**. It only syncs in Game Mode, not Desktop Mode. If only one side changed, the newer copy wins; if both did, it asks you to keep the local copy or use the server's before the game starts. It keeps named save slots with version history.

Tender syncs save RAM from **RetroArch cores in RetroDECK** only. Standalone emulator saves aren't supported yet, and save states are left out by design.

| Coverage       | Systems                                                                                                                                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅ Synced      | NES/Famicom/FDS, SNES/Super Famicom, GB/GBC/GBA, N64, NDS, Master System, Game Gear, SG-1000, Genesis/Mega Drive, 32X, Saturn, PC Engine/TurboGrafx-16/PC-FX, WonderSwan, Neo Geo Pocket, Pokémon Mini, Virtual Boy, Atari 2600, C64, FBNeo, TIC-80 and others |
| ⚠️ Partly       | Sega CD (raw `.bin` only), Amiga CD32 (`.chd` only)                                                                                                                                                                                         |
| ❌ Not yet      | PS1 (planned), 3DO and Neo Geo (in development)                                                                                                                                                                                              |
| ❌ Not synced   | PS2, Dreamcast, GameCube/Wii, 3DS, Wii U, PSP, MAME, DOS, ScummVM                                                                                                                                                                             |

### RetroArch Sync

RetroArch Sync syncs saves and states for **any RetroArch core**: on connect, when RetroArch closes, whenever a save file changes and when it reconnects. It needs RetroArch's network commands turned on (port 55355). The default conflict setting prefers the newer copy; you can switch it to always local, always server or ask every time. The local copy is backed up before it's overwritten.

It finds RetroArch installed natively, as a Flatpak, Snap or AppImage, through Steam or inside RetroDECK, or at a custom path. It's Linux-only: there's no Windows, macOS or Android build.

Development of RetroArch Sync's sync engine has moved to the same author's new app, [Ludo](https://github.com/Covin90/ludo), which also runs as a Steam Deck plugin.

### Apps Without Save Sync

SwitchRomM doesn't sync saves or states.

## Other Community Tools

These projects from the README's community list work with RomM but aren't game clients:

- **[Syncthing sync](https://github.com/amn-96/romm_syncthing_sync)** (v1.4.1): a background service that watches a Syncthing folder and uploads saves and states from it to RomM, including state screenshots. It's one-way, from the folder to RomM, and never uploads ROMs. It matches files to games by platform folder and filename, and targets RetroArch setups (Android, muOS, Knulli) and MinUI/NextUI.
- **[romm-comm](https://github.com/idio-sync/romm-comm)**: a Discord bot for searching your library and posting download links, announcing newly added games, a RetroAchievements leaderboard for your RomM users, game requests, Netplay lobbies, and admin commands for scans and user management. It doesn't download or sync anything itself.
- **[GGRequestz](https://github.com/XTREEMMAK/ggrequestz)** (v1.5.0): a self-hosted game discovery and request tracker. It reads your RomM library to mark requested games you already have and link to them, and never writes to RomM.

## See Also

- [First-Party Apps](first-party-apps.md): setup for Argosy, Grout and the Playnite plugin
- [Saves & States](../using/saves-and-states.md): how saves and states work in RomM itself
- [Device Sync Protocol](../developers/device-sync-protocol.md): the API these apps sync through
- [Community section in the README](https://github.com/rommapp/romm/#community): the current list of community apps
