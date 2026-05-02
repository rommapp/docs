---
title: Console Mode
description: TV + gamepad UI for RomM
---

# Console Mode

**Console Mode** is a second UI for RomM, living at `/console`, designed for TV screens and gamepad input. It runs on the same instance with the same data, just a completely different UX.

If you're on a desktop with a keyboard and mouse, you probably don't need it. The main library view is your home. But if you're on a TV with RomM on a stick / Shield / Pi / mini-PC, a handheld running muOS / Knulli / Batocera / Steam Deck, or a browser tab full-screened with a gamepad plugged in, Console Mode is where you want to be.

## Input

Console Mode supports gamepads (Xbox, PS, 8BitDo, Steam Controller, Switch Pro: anything the browser sees as a standard gamepad), keyboards as a fallback, and touch on handhelds without native gamepad input.

Button labels in the UI follow the Xbox convention regardless of actual controller, so "A" is always the bottom face button.

## Available features

Most of the main UI's features are available in Console Mode:

- Browse library, platforms, collections
- Search and filters
- Play (launches [In-Browser Play](in-browser-play/emulatorjs.md) or offers a download if the platform isn't browser-playable)
- Saves and states: upload, select, delete
- Smart and virtual collections
- RetroAchievements progression display

Not yet in Console Mode (still use the main UI):

- ROM editing (match, edit metadata)
- Scanning
- Administration (users, tasks, stats)
- ROM Patcher

## Handheld-specific notes

Running on muOS / Batocera / Knulli / a Steam Deck? Consider:

- **[Grout](../ecosystem/first-party-apps.md#grout)**: official handheld companion that syncs saves/states to/from the device
- **[Argosy Launcher](../ecosystem/first-party-apps.md#argosy-launcher)**: Android handhelds that can run a browser but want a native-feeling app

Both use [Client API Tokens](../developers/client-api-tokens.md) for auth.

## Known limitations

- **Admin features aren't available**: if you're the admin, flip back to the main UI for scans / user management.
- **Mobile browsers with no gamepad**: touch works but the UX is designed for gamepads, not fingers. Use the main UI or the Argosy mobile app ([Ecosystem](../ecosystem/first-party-apps.md#argosy-launcher)).

## Troubleshooting

- **Gamepad not detected**: Chrome sometimes needs a button press on the page before enumerating gamepads. Press any button and it'll show up.
- **Laggy navigation**: low-powered device running a heavy browser. Try Firefox or a lighter browser build.

More in [Troubleshooting](../troubleshooting/index.md).
