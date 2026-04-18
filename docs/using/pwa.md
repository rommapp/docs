---
title: Install as PWA
description: Add RomM to your phone or desktop home screen for an app-like experience.
---

# Install as PWA

RomM ships as a **Progressive Web App**: a proper manifest, service worker, and icons. You can install it to your phone or desktop and launch it like a native app. Same RomM, no browser chrome.

New in 5.0.

## Why install?

- **Looks and feels native**: icon on your home screen, fullscreen by default.
- **Faster startup**: the service worker caches the shell.
- **Mobile-friendly**: no browser address bar eating vertical space.
- **Offline-ish**: you can open the app without a network, though anything that actually fetches data still needs the server.

## Install on Android

### Chrome

1. Open your RomM URL in Chrome.
2. Tap the **three-dot menu** → **Install app** (or "Add to Home screen" on older Chrome).
3. Confirm.

An icon appears on your home screen. Launching opens RomM full-screen.

### Samsung Internet / Other Android browsers

Similar: look for "Add to Home screen" in the share / menu.

## Install on iOS

iOS Safari is slightly different and has no true PWA parity (some APIs are missing), but the basic install flow works:

1. Open your RomM URL in **Safari** (not Chrome; on iOS, Chrome uses Safari's engine but doesn't expose the install flow).
2. Tap the **Share** button (square with arrow).
3. **Add to Home Screen**.
4. Name it, tap **Add**.

The icon appears on your home screen. Launching opens RomM in a standalone Safari view.

iOS limitations:

- No push notifications.
- Service worker caching is more aggressive / unpredictable than on Android.
- The browser UI is fully gone; only gesture-based navigation.

## Install on desktop

### Chrome / Edge / Brave

1. Open RomM.
2. Look for the **install icon** in the address bar (small computer with a down-arrow, on the right).
3. Click → **Install**.

App launches in its own window, separate from the main browser. Pin to taskbar / dock as you would any other app.

### Firefox

Firefox desktop doesn't install PWAs out of the box. Workarounds:

- Use a [Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/pwas-for-firefox/) like PWAsForFirefox.
- Or just use Chrome / Edge for the PWA.

### Safari (macOS 14+)

1. Open RomM in Safari.
2. **File** menu → **Add to Dock**.

Same standalone window treatment as Chrome.

## Uninstalling

- **Android**: long-press the icon → **Uninstall** (or **Remove from Home screen**).
- **iOS**: long-press → **Remove App**.
- **Desktop**: inside the installed PWA window → three-dot menu → **Uninstall RomM**.

Uninstalling just removes the shortcut and cached shell. Nothing server-side is touched.

## Updating

The service worker checks for new versions on launch. If RomM updates, the next time you open the PWA you get the latest shell. Browser-managed; no manual action.

If a stale shell is causing issues (e.g. seeing old UI after an upgrade), force-refresh:

- **Chrome/Edge mobile**: long-press the reload button → **Hard Reload**.
- **iOS Safari**: Settings → Safari → Clear History and Website Data also removes the PWA cache.
- **Desktop PWAs**: the three-dot menu usually has a Reload option; hold Shift for a hard reload.

## Limitations

- **Requires HTTPS**: PWAs don't install from plain-HTTP hosts. Make sure your RomM is behind a reverse proxy with TLS. See [Reverse Proxy](../install/reverse-proxy.md).
- **Icons**: RomM ships 192×192 and 512×512 manifest icons. Some devices pick a mid-size fallback that looks slightly blurry; known limitation, we'll expand the icon set over time.
- **No push notifications yet**: the PWA manifest doesn't register a notification handler in 5.0. Scan completion, task failures, etc. don't notify you.
- **Offline mode is partial**: opening the installed PWA offline shows the shell, but you can't actually browse the library or play anything without the server reachable.

## Use with Console Mode

PWA + [Console Mode](console-mode.md) is a powerful combo:

- Install the PWA on a TV-attached Android box, then set default view to `/console`.
- Launching the app goes straight to a gamepad-friendly library. Feels like a console.

## Troubleshooting

- **No Install option in Chrome**: RomM isn't on HTTPS, or the manifest is missing/broken. Open devtools → Application → Manifest to diagnose.
- **Icon shows as a generic globe**: manifest icons aren't loading. Check the image URLs in devtools → Application → Manifest.
- **App won't open offline**: expected; only the shell caches, not data. Network access is required for everything useful.

## Want a native app instead?

Community-made native apps are listed on [Ecosystem → Community Apps](../ecosystem/community-apps.md), including Argosy Launcher, RommBrowser, and more. PWA is the zero-install path; native apps give you platform integration (notifications, deeper OS hooks) where it matters.
