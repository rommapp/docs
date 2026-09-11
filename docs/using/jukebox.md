---
title: Jukebox
description: A soundtrack player across your whole library
---

# Jukebox

The Jukebox is a music player over every soundtrack in your library at once, rather than per game. It is a **beta feature**, so expect it to move around between releases.

## Where the tracks come from

Tracks are audio files in a `soundtrack/` subfolder of a game's folder, one of the [recognised subfolders](../getting-started/folder-structure.md#multi-file-games) alongside `manual/` and `walkthrough/`:

```text
roms/snes/chrono trigger/
├─ chrono trigger.sfc
└─ soundtrack/
   ├─ 01 - Chrono Trigger.flac
   └─ 02 - Memories of Green.flac
```

`.mp3`, `.ogg`, `.oga`, `.opus`, `.m4a`, `.aac`, `.wav` and `.flac` are read. Scanning parses each file's tags for the title, artist, album, genre, year, track number and duration, and pulls out an embedded cover if there is one, so a well-tagged rip browses properly without any work on your part. Files with no tags fall back to their filename.

Soundtrack files never carry a ROM binary, so they are skipped by hashing and by title-id extraction, and they don't affect how the game itself is matched.

## Browsing

The same track library is faceted several ways, each of which is also the typeahead behind its search box:

| Facet      | What it groups by                                                |
| ---------- | ---------------------------------------------------------------- |
| Album      | The album tag                                                    |
| Game       | The game the tracks belong to, which is the jukebox's album list |
| Platform   | The game's platform                                              |
| Artist     | The artist tag                                                   |
| Genre      | The genre tag                                                    |
| Game genre | The genre of the _game_, not of the music                        |
| Year       | The year tag                                                     |

Everything you can see follows your normal library visibility, so a platform hidden from you contributes no tracks.

## Mixes and playlists

Four generated shelves need no setup:

- **Free Radio** picks a randomised, album-balanced hour, so one long soundtrack can't take the whole set over.
- **Decade Mix** groups by release decade.
- **Recently added** is the newest tracks in the library.
- **Favourites** is your own starred tracks.

Beyond those, you can build playlists of your own: ordered, renameable, and either private or visible to everyone on the instance. Favourites and playlists need the `playlists.read` and `playlists.write` permissions, browsing needs only `roms.read`.

The player keeps shuffle on across sessions rather than resetting it per queue, collapses to a mini player so it keeps going while you browse, and offers play, favourite, download and delete on each track.

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

Playlists live under `/music/playlists`, with the usual create, read, update and delete, plus `/{id}/tracks` to list, append and remove, and `/{id}/tracks/order` to reorder.

## Related

- [Folder Structure](../getting-started/folder-structure.md#multi-file-games): where a `soundtrack/` folder goes
- [Uploads](uploads.md): adding tracks through the web UI
