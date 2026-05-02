---
title: Mobile & TV
description: Use phones, tablets, TVs, and handhelds
---

# Mobile & TV

RomM is a web app. Anything with a modern browser can use it: phones, tablets, handhelds, TVs, set-top boxes. This page walks through the recommended setup for each form factor.

## Phones and tablets

### Option A: the PWA

Install RomM as a Progressive Web App via your browser's add-to-home-screen flow, the recommended path for most mobile users: feels native, launches from the home screen, no app store. Requires HTTPS.

- Good for: browsing, managing your library, downloading ROMs, in-browser play on devices with enough horsepower
- Limited by: no push notifications (yet), no OS-level file pickers for ROM uploads (use the web UI instead), Safari quirks on iOS

### Option B: a native app

[Community-maintained mobile apps](https://github.com/rommapp/romm/#community) exist:

- **Argosy Launcher** (Android): official first-party. ROM syncing and launching
- **romm-ios-app** / **romm-mobile**: community iOS and Android clients

Native apps give you proper file pickers, OS notifications, and nicer integration with device-level emulators (RetroArch mobile, Delta on iOS, etc.).

### Browser choice

- **Android**: Chrome, Firefox, or Samsung Internet. Chrome has best PWA support.
- **iOS**: Safari (the only way to install as PWA on iOS)

### Touch vs mouse

The main UI handles touch gracefully. [Console Mode](console-mode.md) is gamepad-first but works with touch on handhelds that lack a gamepad.

## TVs and set-top boxes

You've got a TV-attached Android box, a mini-PC, a Nvidia Shield, or a browser running on the TV itself. The combo:

### The setup

1. **Install RomM as a PWA** on the device's browser.
2. **Set the default view to Console Mode** in your profile preferences.
3. **Plug in a gamepad**: USB, Bluetooth, anything the browser sees.
4. **Launch the PWA.** You're in Console Mode, gamepad-ready.

Now it looks and feels like a console UI, running on a web page. Launching a game loads EmulatorJS full-screen, and the same gamepad passes through.

### What about actual emulation?

Most TVs and cheap Android boxes don't have the horsepower for heavy in-browser emulation (Saturn, Dreamcast, PSP). Two workarounds:

1. **Lighter cores**: EmulatorJS works fine on most platforms up to 16-bit and N64 on modest hardware. Stick to older systems and it's great.
2. **Native companion app**: install [RetroArch](https://retroarch.com/) or another emulator on the device, and sync ROMs/saves to it via a companion app (Argosy, DeckRommSync, etc.). The library management + your native emulator's playback.

## Handhelds

Handhelds running custom firmware (muOS, Batocera, Knulli, ArkOS, JELOS, ROCKNIX) aren't traditional clients. They don't run browsers well, and you probably don't want to play in one anyway. The integration pattern is:

1. **Library hosted** on your home server.
2. **A companion app on the handheld** syncs ROMs, saves, and states bidirectionally.
3. **The handheld plays games locally** using its native emulators (RetroArch et al.).

Recommended companions:

- **[Grout](../ecosystem/first-party-apps.md#grout)**: first-party. muOS and NextUI handhelds
- **[DeckRommSync](https://github.com/rommapp/romm/#community)**: Steam Deck (SteamOS)
- **[SwitchRomM](https://github.com/rommapp/romm/#community)**: Nintendo Switch (homebrew)

All of these use [Client API Tokens](../developers/client-api-tokens.md) for auth and the [Device Sync Protocol](../developers/device-sync-protocol.md) for the actual data transfer.

## Steam Deck

Two ways to use it on a Deck:

### Desktop mode

Any browser works. Use the PWA install flow (same as desktop) for a dedicated launcher.

### Via DeckRommSync

Syncs ROMs and saves to the Deck's local library so RetroArch / EmuDeck picks them up natively. Set up once, then play without RomM in the loop. See the [Community section in the RomM README](https://github.com/rommapp/romm/#community).

Best combo: DeckRommSync for saves, plus the PWA for browsing / managing the library.

## Bandwidth considerations

Some things are bandwidth-hungry, some aren't:

| Activity             | Typical bandwidth   | Notes                                                                                    |
| -------------------- | ------------------- | ---------------------------------------------------------------------------------------- |
| Browsing the library | Low                 | Cover-art thumbnails, a few hundred KB per page load.                                    |
| Playing in browser   | Medium              | ROM streams at boot, then cached. PSP / Saturn ISOs can be hundreds of MB on first load. |
| Netplay              | Medium–High         | Video stream from host to players. ~500 kbps for SNES, more for higher-res cores.        |
| Bulk download        | As-much-as-you-want | Rate-limited only by your reverse proxy and network.                                     |
| Device sync (saves)  | Low                 | Saves are small, so sync is fast.                                                        |
| Device sync (ROMs)   | High                | Pushing full ROM sets to a handheld initially is a lot.                                  |

On cellular? Set `DISABLE_DOWNLOAD_ENDPOINT_AUTH=false` (default: keep auth on) to avoid accidental discovery, and prefer native companion apps over in-browser play.

## Self-hosting tips

If you host RomM on a home server and want to reach it from cellular:

- Put it behind a reverse proxy with TLS (see [Reverse Proxy](../install/reverse-proxy.md)).
- Use a VPN (Tailscale, WireGuard) instead of exposing to the internet. Handhelds with Tailscale setups "just work".
- For public access without a VPN, put Cloudflare Access or similar zero-trust auth in front. Disable `ALLOW_PUBLIC_REGISTRATION` because the edge auth handles gatekeeping.

## See also

- [Console Mode](console-mode.md)
- [Integrations & Ecosystem](../ecosystem/index.md): every supported companion app
- [Community section in the RomM README](https://github.com/rommapp/romm/#community): the full list with platform / status flags
