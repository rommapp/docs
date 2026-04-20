---
title: EmulatorJS Configuration
description: Operator-level tuning of the EmulatorJS player, per-core settings, controls, cache, Netplay.
---

# EmulatorJS Configuration

End-user side of EmulatorJS lives in [In-Browser Play](../using/in-browser-play.md). This page is **operator-facing**: how to tune EmulatorJS via `config.yml` for every user on your instance.

All settings below live under the `emulatorjs:` key in [`config.yml`](../reference/configuration-file.md#emulatorjs).

## Enable / disable

```yaml
environment:
    - ENABLE_EMULATORJS=true # default
```

Set to `false` to disable EmulatorJS entirely: useful on the slim image or when running headless with companion apps only. The Play button is hidden but Ruffle still works independently. See [Image Variants](../install/image-variants.md).

## Debug mode

```yaml
emulatorjs:
    debug: true
```

Logs every available option for each core to the browser console when a game launches. Turn on when tuning, and turn off in production (it's verbose).

## Cache limit

```yaml
emulatorjs:
    cache_limit: 52428800 # 50 MB per ROM
```

Each ROM's cache (core files, BIOS, settings) is capped. `null` removes the cap: useful for large PSP / Saturn libraries on hosts with plenty of disk.

## DOS-specific toggles

```yaml
emulatorjs:
    disable_batch_bootup: true
    disable_auto_unload: true
```

- **`disable_batch_bootup`**: skips the `autorun.bat` step when `dosbox-pure` loads. Try this if DOS games hang on boot. See [MS-DOS](ms-dos.md).
- **`disable_auto_unload`**: keeps the emulator running when the user navigates away. Default off (browsers unload the emulator on page change)

## Netplay

```yaml
emulatorjs:
    netplay:
        enabled: true
        ice_servers:
            - urls: "stun:stun.l.google.com:19302"
            - urls: "turn:openrelay.metered.ca:443"
              username: "openrelayproject"
              credential: "openrelayproject"
```

Full Netplay config in [Configuration File → `emulatorjs.netplay`](../reference/configuration-file.md#emulatorjsnetplay-new-in-50) and user-side docs in [Netplay](../using/netplay.md).

<!-- prettier-ignore -->
!!! warning "Nightly CDN caveat"
    Enabling Netplay switches some assets to EmulatorJS's nightly CDN. Occasional hiccups are possible. If you don't need Netplay, leave it off.

## Per-core settings

Every core exposes different options. Set defaults your users get pre-filled:

```yaml
emulatorjs:
    settings:
        # Apply to all cores
        default:
            fps: show

        # Per-core
        snes9x:
            snes9x_region: ntsc
            snes9x_layer_1: true
            snes9x_overclock: false

        parallel_n64:
            vsync: disable
            parallel-n64-gfxplugin: "auto"

        ppsspp:
            ppsspp_internal_resolution: "2" # 2x
            ppsspp_frame_skipping: "0"
```

Finding core names and their options:

1. Turn on `debug: true` temporarily.
2. Load a game in that core.
3. Browser console → filter for "option".
4. Copy the keys you care about.

Upstream reference: [EmulatorJS core options](https://emulatorjs.org/docs4devs/settings/).

## Control mapping

```yaml
emulatorjs:
    controls:
        snes9x:
            0: # player 1
                0: # B button slot (index 0)
                    value: x # keyboard key "x"
                    value2: BUTTON_2 # controller button 2
                1: # Y button slot
                    value: z
                    value2: BUTTON_3
            1: # player 2
                0:
                    value: /
                    value2: BUTTON_2
```

The structure:

- Top level = core name
- Second level = player number (`0`, `1`, `2`, `3`)
- Third level = button slot (core-specific, and 0 is usually the first face button).
- `value` = keyboard key
- `value2` = gamepad button

Slot indexes and what they map to vary per core. See [EmulatorJS control-mapping docs](https://emulatorjs.org/docs4devs/control-mapping/).

Users can override operator-level defaults in-game via Menu → **Controls**. Operator-level just sets the starting point.

## Example: 2-player SNES setup

```yaml
emulatorjs:
    settings:
        snes9x:
            snes9x_region: ntsc
    controls:
        snes9x:
            0: # P1 on keyboard (WASD cluster)
                0: { value: ",", value2: "BUTTON_2" } # B
                1: { value: ".", value2: "BUTTON_3" } # A
                2: { value: "l", value2: "BUTTON_1" } # Y
                3: { value: "p", value2: "BUTTON_4" } # X
            1: # P2 on arrows + numpad
                0: { value: "/", value2: "BUTTON_2" }
                1: { value: "'", value2: "BUTTON_3" }
```

## Per-user vs operator-level

| Where the setting is stored       | Who it affects       | Survives upgrades? |
| --------------------------------- | -------------------- | ------------------ |
| Operator: `config.yml` / env vars | Everyone, as default | Yes                |
| Per-user: in-game Menu → Settings | Just that user       | Yes                |
| Per-user: in-game Menu → Controls | Just that user       | Yes                |

Per-user overrides take precedence. A config.yml setting is the fallback.

## Pre-built config examples

For frontend parity:

- [`config.batocera-retrobat.yml`](https://github.com/rommapp/romm/blob/master/examples/config.batocera-retrobat.yml): Batocera / RetroBat control + setting layouts
- [`config.es-de.example.yml`](https://github.com/rommapp/romm/blob/master/examples/config.es-de.example.yml): ES-DE layout

## Troubleshooting

- **Settings don't apply.** `debug: true`, reload a game, check console for "option set" logs. Core name might be wrong.
- **Netplay breaks after enabling.** See [Netplay Troubleshooting](../troubleshooting/netplay.md).
- **Control map works in one game, not another.** Different cores. Check you've set the right core name for the platform.

## See also

- [In-Browser Play](../using/in-browser-play.md): end-user-facing
- [Configuration File → `emulatorjs`](../reference/configuration-file.md#emulatorjs): full schema
- [EmulatorJS docs](https://emulatorjs.org/docs/): upstream reference
