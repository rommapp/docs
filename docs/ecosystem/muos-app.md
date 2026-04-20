---
title: muOS App
description: Official RomM app for muOS and EmulationStation handhelds, fetch games wirelessly.
---

<!-- trunk-ignore-all(markdownlint/MD033) -->

# muOS App

<div align="center">
    <img src="../../resources/romm/integrations/muos.svg" height="200px" width="200px" alt="RomM muOS logo">
</div>

[muOS](https://muos.dev) is a custom firmware (CFW) for handheld devices: Anbernic, Miyoo, and similar. The **muOS App** connects to your RomM instance and fetches ROMs wirelessly.

- **Repo:** [rommapp/muos-app](https://github.com/rommapp/muos-app)
- **Platforms:** muOS, EmulationStation (via PortMaster)
- **Use case:** fetch games on-demand from RomM without cable-swapping SD cards.

## muOS-specific flavour vs Grout

This page covers the **muOS App**: a lightweight client focused on game fetching. For the fuller push/pull sync experience (saves back to RomM, play-session reporting), use [Grout](grout.md) instead. They're two different clients for the same family of devices.

- **muOS App**: lightweight, pulls ROMs, no save sync
- **Grout**: full sync, ROMs + saves + states + play sessions

Pick based on what you need.

## Installing: muOS

Installation uses muOS's [Archive Manager](https://muos.dev/installation/archive):

1. Download the latest `RomM.muOS.x.x.x.muxapp` from [GitHub Releases](https://github.com/rommapp/muos-app/releases/latest).
2. Move the `.muxapp` file to `/mnt/mmc/ARCHIVE/` on the device (USB, SD swap, or SSH).
3. On the device: **Applications → Archive Manager** → select `RomM.muOS.x.x.x.muxapp` → install.
4. Once installed, copy `/mnt/mmc/MUOS/application/RomM/env.template` to `.env` in the same folder.
5. Edit `.env` (SSH works well, as does any method that writes to SD card):

    ```dotenv
    HOST=http://192.168.1.100:3000
    USERNAME=yourusername
    PASSWORD=yourpassword
    ```

6. Launch from **Applications → RomM** on the device.

<!-- prettier-ignore -->
!!! tip "Use a dedicated account or token"
    The username/password lives in plaintext on the SD card. Use a dedicated Viewer-role account for the handheld, not your admin credentials.

    Once RomM's 5.0 Client API Token flow is wired into the muOS app (planned), prefer pairing via token instead of password.

## Installing: EmulationStation (via PortMaster)

For EmulationStation-based devices:

1. Download the `RomM App.sh` file and the `RomM/` folder.
2. Copy to `roms/ports/` on the device.
3. SSH / shell in: `chmod +x "RomM App.sh"`.
4. Launch EmulationStation → **Ports** → RomM App.

## Network requirements

The handheld has to reach your RomM instance over Wi-Fi.

Simplest setup:

- **Same LAN.** Handheld and RomM server on the same SSID. `HOST` = server IP + port
- **Plain HTTP works** on a trusted LAN, and no reverse proxy is needed.

More-involved setups:

- **Reverse proxy with TLS.** `HOST=https://romm.example.com`. HTTPS works but introduces cert-validation risk on handhelds (some fail strict TLS).
- **Remote access via VPN.** Install Tailscale or similar on the handheld (if supported). This lets the handheld reach RomM from outside the LAN.

## Using the app

Launch RomM app → browse platforms → select a game → download.

Downloaded games appear in the device's usual ROM folder for the platform, so muOS / ES picks them up on the next library refresh.

## What it doesn't do (yet)

- **Save sync.** This app is pull-only. For bidirectional sync, use [Grout](grout.md).
- **Play session tracking.** Not ingested into RomM
- **Firmware download.** Not in scope

If you need these, Grout is the app.

## Troubleshooting

- **Can't connect.** Wrong `HOST` in `.env`, or the handheld isn't on the same network as RomM. Ping RomM's IP from the handheld's shell to confirm reachability.
- **"Authentication failed".** Password wrong, or `DISABLE_USERPASS_LOGIN=true` on the RomM side. Either re-enable user/pass login or use a token once supported.
- **Downloaded games don't show in the platform.** Refresh the library from muOS's UI. If they still don't appear, the platform folder in `HOST_PATH` is wrong. Check muOS's expected layout.

## See also

- [Grout](grout.md): the fuller sync client for the same device family
- [Client API Tokens](client-api-tokens.md): safer auth than plaintext credentials in `.env`
- [Mobile & TV](../using/mobile-and-tv.md): handheld usage patterns
- [rommapp/muos-app](https://github.com/rommapp/muos-app): source, issues, releases
