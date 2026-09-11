---
title: Walkthroughs
description: Attach guides to a game and track where you left off
---

# Walkthroughs

Walkthroughs are documents attached to a game, handled the same way manuals are. Upload your own, or paste in a GameFAQs URL and RomM will fetch the guide for you. It tracks how far through you are, per user, and shows that as a progress bar.

You need `roms.write` to add or delete one. Reading a walkthrough and tracking your own progress only needs read access.

## Where they live

Walkthroughs are files in a `walkthrough/` subfolder of the game's own folder, next to the other [recognised subfolders](../getting-started/folder-structure.md#multi-file-games) like `manual/` and `soundtrack/`:

```text
roms/snes/chrono trigger/
├─ chrono trigger.sfc
├─ manual/
│  └─ chrono trigger.pdf
└─ walkthrough/
   ├─ chrono-trigger-guide.txt
   └─ boss-faq.md
```

If the game is a single file on disk, uploading a walkthrough converts it to a folder first so there's somewhere to put the document.

These are just files in your library. They survive rescans, they're covered by your backups, and you can copy them in from the filesystem instead of uploading if you'd rather.

Accepted formats: `.pdf`, `.md`, `.txt`, `.html`, `.htm`. HTML gets sanitised on the way in and is served under a sandboxing CSP on the way out.

## Importing from GameFAQs

Paste in a GameFAQs URL and RomM pulls out the title, author and body, then saves the lot as **plain text**. None of the remote HTML is kept or served.

The URL has to be `https` and on one of GameFAQs' own hosts (`gamefaqs.gamespot.com`, `www.gamefaqs.com`, `gamefaqs.com`). Guides over 8 MiB are rejected.

This only works on the old-style text guides, the ones that render inside a `<pre>` block. If a guide is published as a proper HTML page there's no plain text to extract and the import fails, so save it yourself and upload it.

## Reading progress

RomM stores how far you've scrolled (0 to 1) and, for paged formats, which page you're on. That's what the progress bar reads.

It's kept server-side rather than in the browser, so opening a guide on your phone picks up where you left off on your desktop. Tracking is per document, which means two guides for the same game don't interfere.

## API

| Method   | Path                                      | Description                                     |
| -------- | ----------------------------------------- | ----------------------------------------------- |
| `POST`   | `/roms/{id}/walkthroughs/files`           | Upload a walkthrough document                   |
| `POST`   | `/roms/{id}/walkthroughs/gamefaqs`        | Import one from a GameFAQs URL, as plain text   |
| `DELETE` | `/roms/{id}/walkthroughs/files/{file_id}` | Delete a walkthrough                            |
| `GET`    | `/roms/{rom_id}/files/{file_id}/progress` | The requester's reading progress for a document |
| `PUT`    | `/roms/{rom_id}/files/{file_id}/progress` | Record reading progress                         |

The upload endpoint streams the body and wants the filename in an `x-upload-filename` header, optionally with `x-doc-title` and `x-doc-author`. The progress endpoints always act on the calling user, so there's no user id to pass and no way to read someone else's position.

## Related

- [Folder Structure](../getting-started/folder-structure.md#multi-file-games): the other subfolders a game folder can carry
- [Uploads](uploads.md): how files reach the library
