---
title: Argosy Launcher
description: Official Android launcher for RomM, browse and launch your library on mobile.
---

# Argosy Launcher

**Argosy Launcher** is RomM's first-party Android app: browse your library, download ROMs on the fly, and launch into RetroArch or your emulator of choice.

- **Repo:** [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher)
- **Language:** Kotlin
- **License:** GPL-3.0
- **Platforms:** Android

## What it does

- Browses your full RomM library from an Android device.
- Handles authentication via [Client API Tokens](client-api-tokens.md), paired over a short code so you don't type a 44-character string.
- Downloads ROMs on demand to your device's storage.
- Launches RetroArch (or another configured emulator) with the downloaded ROM.
- Syncs saves / states back to RomM when you finish a session (optional).

## Installing

### From a release

1. Grab the latest `.apk` from [GitHub Releases](https://github.com/rommapp/argosy-launcher/releases/latest).
2. Install via your Android device's package installer (you may need to enable "Install from unknown sources" in Settings).

### Via F-Droid / Play Store

Not currently on either, so APK sideloading is the path for now.

## First-time setup

1. Launch Argosy.
2. Enter your RomM URL (e.g. `https://romm.example.com`), which needs HTTPS in production.
3. Choose **Pair Device**.
4. Argosy shows a pairing URL or QR code: open it on a device that's already signed into RomM.
5. On that device, RomM shows a confirmation dialog; enter the 8-digit code Argosy displayed.
6. Accept, and Argosy receives a Client API Token bound to your RomM account.

From here, Argosy lists your library. Full pairing-flow details in [Client API Tokens](client-api-tokens.md).

## Using Argosy

### Browse

The main view mirrors RomM's platform-and-collection layout: tap a platform to see its games, and search works the same as the RomM web UI.

### Download and launch

Tap a game → **Download** and Argosy pulls the ROM to device storage. Once downloaded, **Play** launches it with your configured emulator.

### Emulator configuration

Argosy → Settings → Emulators. For each platform:

- Pick the external emulator app (RetroArch, Duckstation, PPSSPP, etc.).
- Optionally pass core-specific args.

RetroArch users: Argosy can auto-detect installed RetroArch cores and map platforms to them.

### Save sync

Argosy → Settings → Sync. Two modes:

- **On session end**: uploads saves back to RomM when you exit the emulator.
- **Manual**: you tap Upload when you want.

Saves show up in RomM's **Game Data** tab on the game, same as in-browser saves: see [Saves & States](../using/saves-and-states.md).

## Permissions

Argosy needs:

- **Storage**: to save downloaded ROMs.
- **Network**: to talk to your RomM instance.
- **Optional: Notifications**: download-complete and sync-complete pings.

No other permissions: the app doesn't request contacts, camera, location, or anything else.

## Troubleshooting

- **Can't connect to RomM**: check the URL (including `https://`) and that the RomM instance is reachable from your mobile network. Cellular might be blocked, so try Wi-Fi first.
- **Token invalid**: pair again, since tokens can expire or be revoked on the RomM side.
- **Emulator won't launch**: make sure the emulator app is installed and Argosy has permission to open it; some emulators require an intent-filter setup.
- **Downloads fail partway**: usually network, and Argosy resumes on retry.

Full sync-specific debugging in [Device Sync Troubleshooting](../troubleshooting/sync.md).

## See also

- [Client API Tokens](client-api-tokens.md): the auth + pairing flow Argosy uses.
- [Device Sync Protocol](device-sync-protocol.md): how saves sync.
- [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher): source, issues, releases.
