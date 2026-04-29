---
title: Console Mode
description: TV + gamepad UI for RomM. Spatial navigation, SFX, focus sounds, no mouse needed.
---

# Console Mode

**Console Mode** is a second UI for RomM, living at `/console`, designed for TV screens and gamepad input. Same instance, same data, completely different UX.

New in 5.0. If you're on a desktop with a keyboard and mouse, you probably don't need it. The main [Library](library.md) view is your home. But if you're on:

- A TV with RomM on a stick / Shield / Pi / mini-PC,
- A handheld running muOS / Knulli / Batocera / Steam Deck,
- A browser tab full-screened with a gamepad plugged in,

…you want Console Mode.

## Getting there

Three ways:

1. **Menu bar → Console icon** (looks like a small controller)
2. Type `/console` after your RomM URL: `https://demo.romm.app/console`.
3. Set the default view to Console Mode in **Profile → User Interface → Default view**. This signs you in straight into `/console` every time.

Bookmarking `/console` on your TV browser is the most common pattern.

## Navigating

### Gamepad

Standard gamepad API. Xbox, PS, 8BitDo, Steam Controller, Switch Pro: anything the browser sees as a standard gamepad works. Handhelds with native gamepad input (Steam Deck, muOS devices) work out of the box.

Default bindings (most platforms, configurable):

| Button             | Action                        |
| ------------------ | ----------------------------- |
| D-pad / left stick | Move focus                    |
| A (bottom)         | Activate                      |
| B (right)          | Back / cancel                 |
| X (top)            | Play                          |
| Y (left)           | Details / context menu        |
| LB / RB            | Switch tabs or scroll by page |
| LT / RT            | Jump to start / end of grid   |
| Start              | Main menu                     |
| Select / Back      | Filters                       |

Button labels follow the Xbox convention regardless of actual controller: "A" is always the bottom face button.

### Keyboard (fallback)

If you're browsing `/console` without a gamepad for some reason:

| Key           | Action     |
| ------------- | ---------- |
| Arrow keys    | Move focus |
| Enter / Space | Activate   |
| Escape        | Back       |
| `/`           | Search     |
| `f`           | Filters    |

### Touch

Console Mode is gamepad-first but touch works on handhelds without native gamepad input: tap to activate, swipe to scroll.

## What's different from the main UI

### Spatial navigation

Every focusable element is placed on a 2D grid. D-pad Up / Down / Left / Right moves to the visually-nearest focusable element, not the next DOM element. Works the way a TV UI should.

### Focus sounds

Subtle SFX play on focus, activate, and back. Turn off in **Settings → Console Mode → Audio**.

### Bigger hit targets

Cards and buttons are sized for 10-foot viewing. Grids show fewer items per row than the main UI.

### Simpler information density

The game detail view uses full-screen tabs instead of side-by-side panels. Filter panels are dedicated screens rather than popovers.

### Mouse-cursor auto-hide

The cursor disappears after a few seconds of no movement. Wiggle the mouse (or touch the screen) to bring it back.

### Theme

Console Mode uses its own color palette: higher contrast, bigger typography. It follows the main UI's dark/light mode setting but with TV-appropriate rendering.

## Features

Most of the main UI's features are available in Console Mode:

- ✓ Browse library, platforms, collections
- ✓ Search and filters
- ✓ Play (launches [In-Browser Play](in-browser-play.md) or shows a download prompt if the platform isn't browser-playable)
- ✓ Saves and states: upload, select, delete
- ✓ Smart and virtual collections
- ✓ RetroAchievements progression display

Not yet in Console Mode (still use the main UI):

- ROM editing (match, edit metadata)
- Scanning
- Administration (users, tasks, stats)
- ROM Patcher

## Configuring

### Controller mapping

**Settings → Console Mode → Controls.** Rebind any action to any button. Per-user preferences.

### Audio

**Settings → Console Mode → Audio.** Toggle SFX, adjust volume.

### Grid layout

**Settings → Console Mode → Grid size.** Pick small / medium / large card sizes. Large is best for 10-foot viewing, and small is for close viewing on a phone or handheld.

### Background art

**Settings → Console Mode → Backgrounds.** Use the focused game's screenshot as a faded background. Makes Console Mode feel like a proper console UI. Off by default.

## Launching games

Focus a game → press **A** (Play).

If the platform supports [In-Browser Play](in-browser-play.md), the emulator loads full-screen. Controllers and keyboard pass through automatically.

If not, Console Mode shows a **Download** prompt with a QR code for mobile sharing.

### Pre-launch disc/save/state picker

For multi-disc games, Console Mode asks which disc to boot before launching. For games with existing saves/states, you can pick which to resume from. No dialogs in the middle of a session, because everything's picked up front.

## Known limitations

- **Admin features aren't available**: if you're the admin, flip back to the main UI for scans / user management.
- **Some metadata tabs collapse**: the main UI's "Related Games" + "Additional Content" tabs may be merged on the smaller Console detail view.
- **Mobile browsers with no gamepad**: touch works but the UX is designed for gamepads, not fingers. Use the main UI or the Argosy mobile app ([Ecosystem](../ecosystem/first-party-apps.md#argosy-launcher)).

## Handheld-specific notes

Running on muOS / Batocera / Knulli / a Steam Deck? Consider:

- **[Grout](../ecosystem/first-party-apps.md#grout)**: official handheld companion that syncs saves/states to/from the device
- **[Argosy Launcher](../ecosystem/first-party-apps.md#argosy-launcher)**: Android handhelds that can run a browser but want a native-feeling app

Both use [Client API Tokens](../developers/client-api-tokens.md) for auth.

## Troubleshooting

- **Gamepad not detected**: Chrome sometimes needs a button press on the page before enumerating gamepads. Press any button and it'll show up.
- **Cursor stays visible**: you have a USB mouse plugged into a handheld. Unplug it or set **Cursor hide** to "always" in Console settings.
- **Laggy navigation**: low-powered device running a heavy browser. Try Firefox or a lighter browser build.
- **SFX plays during video**: turn it off in **Console → Audio** or lower volume.

More in [Troubleshooting](../troubleshooting/index.md).
