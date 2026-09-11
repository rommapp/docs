---
title: Jukebox
description: A soundtrack player across your whole library
---

# Jukebox

The Jukebox plays every soundtrack in your library as one collection, instead of one game at a time. It's a **beta feature**, so expect bits of it to change between releases.

## Where the tracks come from

Tracks are audio files in a `soundtrack/` subfolder of a game's folder, one of the [recognised subfolders](../getting-started/folder-structure.md#multi-file-games) alongside `manual/` and `walkthrough/`:

```text
roms/snes/chrono trigger/
├─ chrono trigger.sfc
└─ soundtrack/
   ├─ 01 - Chrono Trigger.flac
   └─ 02 - Memories of Green.flac
```

Supported formats are `.mp3`, `.ogg`, `.oga`, `.opus`, `.m4a`, `.aac`, `.wav` and `.flac`.

Scanning reads each file's tags (title, artist, album, genre, year, track number, duration) and grabs the embedded cover if there is one. Drop in a properly tagged rip and it'll browse correctly with no further work. Untagged files just show their filename.

Soundtrack files are skipped by hashing and title-id extraction, and they have no effect on how the game gets matched.

## Browsing

You can slice the track list several ways. Each one also backs the typeahead in its search box:

| Facet      | What it groups by                                                |
| ---------- | ---------------------------------------------------------------- |
| Album      | The album tag                                                    |
| Game       | The game the tracks belong to, which is the jukebox's album list |
| Platform   | The game's platform                                              |
| Artist     | The artist tag                                                   |
| Genre      | The genre tag                                                    |
| Game genre | The genre of the _game_, not of the music                        |
| Year       | The year tag                                                     |

Your normal library visibility applies throughout. A platform you can't see contributes no tracks.

## Mixes and playlists

Four mixes are generated for you, no setup needed:

- **Free Radio**, about an hour of tracks picked at random but balanced across albums, so one long soundtrack can't hog it.
- **Decade Mix**, grouped by release decade.
- **Recently added**, the newest tracks in the library.
- **Favourites**, whatever you've starred.

You can also build your own playlists. They're ordered, you can rename them, and each one is either private or visible to everyone on the instance.

Browsing needs `roms.read`. Favourites and playlists need `playlists.read` and `playlists.write`.

Shuffle stays on between sessions instead of resetting every time you start a new queue, and the player shrinks to a mini player so the music carries on while you browse. Each track has play, favourite, download and delete.

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

- [Folder Structure](../getting-started/folder-structure.md#multi-file-games): where a `soundtrack/` folder goes
- [Uploads](uploads.md): adding tracks through the web UI
