---
title: EasyRPG
description: Play RPG Maker 2000 and 2003 games in the browser
---

# EasyRPG

RPG Maker 2000 and 2003 games run in the browser on the [EasyRPG Player](https://easyrpg.org), an open-source reimplementation of the RPG Maker 2000/2003 engine built to WebAssembly. Put games under the `rpg-maker` platform (an `easyrpg` folder maps to it too) to play them.

<!-- prettier-ignore -->
!!! info "Full image only"
    The player and the free RTP are bundled in the full container image and have no CDN fallback, so RPG Maker games do not play on the slim image (see [Image Variants](../../install/image-variants.md)).

Server owners can turn the player off with `DISABLE_EASYRPG=true` (see [Environment Variables](../../reference/environment-variables.md)).

## Game folders

The player fetches each file of a game as it needs it, so it can't open an archive. A game must be an extracted folder with `RPG_RT.ldb` at its root, the same layout the game shipped in:

```text
roms/rpg-maker/
└── Yume Nikki/
    ├── RPG_RT.ldb
    ├── RPG_RT.lmt
    ├── Map0001.lmu
    ├── CharSet/
    └── Music/
```

Zipped games show up in the library but have no Play button.

## Run-time package

Many games rely on the RPG Maker run-time package (RTP) for shared graphics and sounds instead of shipping them. RomM bundles the free [EasyRPG RTP](https://github.com/EasyRPG/RTP) and hands its files to any game that asks for an RTP asset by its Japanese or translated name. A game's own files always win over the RTP's.

The free RTP is partial: it has system graphics, character sets, music and sounds, but no battle backgrounds and few monsters or battle animations. Games that depend on the RTP play, with assets missing mostly in battles.

## Controls

The player brings its own controls: keyboard, gamepad and on-screen touch buttons.

## Saves

Saves stay in your browser, separately for each RomM account, and don't sync back to the server.

## Related

- [EmulatorJS](emulatorjs.md): the libretro-core player behind most platforms
- [PICO-8](pico-8.md): another native, non-EmulatorJS player
