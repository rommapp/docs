---
title: EasyRPG
description: Play RPG Maker 2000 and 2003 games in the browser
---

# EasyRPG

[EasyRPG Player](https://easyrpg.org/) is an open-source engine for RPG Maker 2000 and 2003 games, and its web build ships with the full container image. It plays games on the `rpg-maker` platform (an `easyrpg` folder maps to it too).

<!-- prettier-ignore -->
!!! important "Games must be extracted folders"
    The web player fetches each file of a game as it needs it, so it can't read a `.zip`, `.7z` or other archive. Extract each game into its own folder under `rpg-maker/`, with `RPG_RT.ldb` at the top of that folder.

```text
roms/rpg-maker/
├─ Yume Nikki/
│  ├─ RPG_RT.ldb
│  ├─ RPG_RT.lmt
│  ├─ Map0001.lmu
│  ├─ CharSet/
│  └─ ...
└─ another game.zip   ← not playable in the browser
```

A game is playable in EasyRPG when `RPG_RT.ldb` is in the game folder itself, which the API exposes as `is_easyrpg_game` on every ROM. Other games on the platform, archives included, can still be downloaded but don't offer browser play.

## The RTP

Many RPG Maker games rely on the RTP (run-time package), a shared set of graphics, sounds and music the original engine installs separately. The [EasyRPG RTP](https://github.com/EasyRPG/RTP), a free replacement under CC-BY-4.0, is bundled and merged into each game, so games that need it start without you supplying one. A game's own files always win over the RTP's.

The free RTP doesn't have every asset of the commercial ones yet, mostly ones used in battles, so a game can show a blank graphic or stay silent where it uses a missing one. Games that bundle their own copy of the assets they use aren't affected.

## Saves

The player keeps a game's saves in the browser while it runs, and they sync with the server through [device sync](../saves-and-states.md), the same way as the other in-browser players. Each save slot (`Save01.lsd`, `Save02.lsd` and so on) syncs as its own save, so a save made in one browser is there when you launch the game in another. They're kept per user, so two RomM accounts on the same browser keep separate slots. EasyRPG has no save states.

## Disabling it

Set `DISABLE_EASYRPG=true` to turn EasyRPG off for everyone, which keeps the games in your library and downloadable but without browser play.

The slim image doesn't bundle the player, so these games need the full image (see [Image Variants](../../install/image-variants.md)).

## API

The player loads everything through one route, `GET /api/roms/{id}/easyrpg/{path}` (`roms.read`):

- `index.json` returns a file index the player reads at boot, built from the game's files with the RTP merged in.
- Any other path returns that file of the game, or the RTP file standing in for it.

It answers `404` when EasyRPG is disabled, the ROM isn't an RPG Maker 2000/2003 game folder, or the caller can't see the ROM.

For more troubleshooting, see [In-Browser Play Troubleshooting](../../troubleshooting/in-browser-play.md).
