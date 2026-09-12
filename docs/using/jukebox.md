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
   └─ 02 - Memories of Green.flac
```

Supported formats are `.mp3`, `.ogg`, `.oga`, `.opus`, `.m4a`, `.aac`, `.wav` and `.flac`.

Scanning reads each file's tags (title, artist, album, genre, year, track number, duration) and grabs the embedded cover if there is one. Drop in a properly tagged rip and it'll display correctly, while untagged files just show their filename.

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

- **Free Radio**, about an hour of tracks picked at random but balanced across albums
- **Decade Mix**, grouped by release decade.
- **Recently added**, the newest tracks in the library.
- **Favourites**, whatever you've starred.

You can also build your own playlists. They're ordered, you can rename them, keep them private, or make them available to everyone on the instance.

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
