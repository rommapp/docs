---
title: Jukebox
description: A soundtrack player across your whole library
---

# Jukebox

The Jukebox plays every soundtrack in your library as one collection. It's currently a **beta feature**, so expect parts of it to change between releases.

Tracks are audio files in a `soundtrack/` subfolder of a game's folder, one of the [recognised subfolders](../getting-started/folder-structure.md#multi-file-games) alongside `manual/` and `walkthrough/`:

```text
roms/snes/chrono trigger/
├─ chrono trigger.sfc
└─ soundtrack/
   ├─ 01 - Chrono Trigger.flac
   ├─ 02 - Memories of Green.flac
   └─ 03 - Wind Scene.spc
```

Supported formats are `.mp3`, `.ogg`, `.oga`, `.opus`, `.m4a`, `.aac`, `.wav` and `.flac`.

Console sound files also work, and play in the browser through [game-music-emu](https://github.com/libgme/game-music-emu): `.spc` for the SNES, and `.vgm`, `.vgz` and `.gym` for the Sega Genesis/Mega Drive and other systems VGM covers. They're much smaller than rips (a whole SNES soundtrack as SPC is about 1 MB). Each file holds one song, so multi-song formats such as `.nsf` and `.gbs` aren't supported. SPC sets often ship as `.rsn` files, which are RAR archives, so extract the `.spc` files into the `soundtrack/` folder first.

Scanning reads each file's tags (title, artist, album, genre, year, track number, duration) and grabs the embedded cover if there is one. Drop in a properly tagged rip and it'll display correctly, while untagged files just show their filename.

Console sound files aren't read for tags yet. They show their filename and have no duration in the library, which also leaves them out of Free Radio and Decade Mix. Their length appears once they start playing.

## Playback

The player hands the playing track to your operating system through the browser's Media Session API, so media keys, the OS media overlay and phone lock screens show the track and its cover and can play, pause, skip and seek. This doesn't work while a console sound file plays.

An opt-in "Resume music after reload" user setting saves the queue and position in the browser and picks the last track up where it stopped after a reload. If it was playing, it starts again on your first click or key press, since browsers block audio that starts on its own. The saved queue is per user and per browser.

## Browsing

Tracks can be browsed several ways:

|            | What it groups by                                                |
| ---------- | ---------------------------------------------------------------- |
| Album      | The album tag                                                    |
| Game       | The game the tracks belong to, which is the jukebox's album list |
| Platform   | The game's platform                                              |
| Artist     | The artist tag                                                   |
| Genre      | The genre tag                                                    |
| Game genre | The genre of the _game_, not of the music                        |
| Year       | The year tag                                                     |

## Mixes and playlists

Four mixes are generated for you:

- **Free Radio**, about an hour of tracks picked at random but balanced across albums.
- **Decade Mix**, grouped by release decade.
- **Recently added**, the newest tracks in the library.
- **Favourites**, whatever you've starred.

You can also build your own playlists. Playlists are ordered, and you can rename them and either keep them private or make them available to everyone on the instance.

## API

Browsing and the facets above:

| Method | Path                                                               | Description                                 |
| ------ | ------------------------------------------------------------------ | ------------------------------------------- |
| `GET`  | `/music/tracks`                                                    | Flat, filterable, paginated track list      |
| `GET`  | `/music/games`, `/music/platforms`, `/music/game-genres`           | Library facets over the soundtracks         |
| `GET`  | `/music/albums`, `/music/artists`, `/music/genres`, `/music/years` | Tag facets, each with counts                |
| `GET`  | `/music/stats`                                                     | Library-wide track count and total duration |
| `GET`  | `/music/favorites`                                                 | The requester's favourite tracks            |
| `POST` | `/music/favorites`                                                 | Mark tracks as favourites                   |

Playlists are under `/music/playlists` with the usual create, read, update and delete. `/{id}/tracks` lists, appends and removes, and `/{id}/tracks/order` reorders.

## Related

- [Uploads](uploads.md): adding tracks through the web UI
