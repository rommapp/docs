---
title: Walkthroughs
description: Attach guides to a game and track where you left off
---

# Walkthroughs

Walkthroughs are documents attached to a game, handled the same way as manuals. Upload your own, or paste in a GameFAQs URL and RomM will fetch the guide for you. It tracks how far through you are, per user, and shows it as a progress bar.

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

If the game is a single file on disk, uploading a walkthrough converts it to a folder first so there's somewhere to put the document. Accepted formats: `.pdf`, `.md`, `.txt`, `.html`, `.htm`. HTML files get sanitised on upload and served under a sandboxing CSP when displayed, to prevent XSS attacks.

## Importing from GameFAQs

Paste in a GameFAQs URL and the title, author and body are extracted, and saved as plain text. The URL has to be `https` and on one of GameFAQs' own hosts (`gamefaqs.gamespot.com`, `www.gamefaqs.com`, `gamefaqs.com`). Guides over 8 MiB are rejected.

This only works on the old-style text guides, the ones that render inside a `<pre>` block. If a guide is published as a proper HTML page there's no plain text to extract and the import fails, so save it yourself and upload it.

## API

| Method   | Path                                      | Description                                     |
| -------- | ----------------------------------------- | ----------------------------------------------- |
| `POST`   | `/roms/{id}/walkthroughs/files`           | Upload a walkthrough document                   |
| `POST`   | `/roms/{id}/walkthroughs/gamefaqs`        | Import one from a GameFAQs URL, as plain text   |
| `DELETE` | `/roms/{id}/walkthroughs/files/{file_id}` | Delete a walkthrough                            |
| `GET`    | `/roms/{rom_id}/files/{file_id}/progress` | The requester's reading progress for a document |
| `PUT`    | `/roms/{rom_id}/files/{file_id}/progress` | Record reading progress                         |

The upload endpoint streams the body and wants the filename in an `x-upload-filename` header, optionally with `x-doc-title` and `x-doc-author`.

## Related

- [Uploads](uploads.md): how files reach the library
