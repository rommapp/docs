---
title: Walkthroughs
description: Attach guides to a game and track where you left off
---

# Walkthroughs

A walkthrough is a document attached to a game, stored and served the same way its manual is. You can upload your own, or hand RomM a GameFAQs URL and let it fetch the guide for you. RomM remembers where each user left off, separately per user, and shows that as reading progress.

Adding and deleting walkthroughs needs the `roms.write` permission. Reading one, and recording your own progress in it, needs only read access.

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

Uploading a walkthrough to a game that is a single file on disk promotes it to a folder first, so the file has somewhere to go. They are ordinary files in your library, so they survive a rescan, get backed up with everything else, and can be dropped in from the filesystem instead of uploaded.

Accepted formats are `.pdf`, `.md`, `.txt`, `.html` and `.htm`. HTML documents are served under a sandboxing content-security policy, on top of being sanitised when they are stored.

## Importing from GameFAQs

Give RomM the URL of a GameFAQs text guide and it fetches the guide, extracts the title, the author and the body, and stores the result as **plain text**. Remote HTML is never stored and never served, so there is nothing script-capable to sanitise in the first place.

Only `https` URLs on GameFAQs' own hosts (`gamefaqs.gamespot.com`, `www.gamefaqs.com`, `gamefaqs.com`) are accepted, and the fetch rides RomM's SSRF-protected HTTP client. Guides larger than 8 MiB are refused.

This works on GameFAQs' plain-text guides, the ones that render inside a `<pre>` block. A guide published as a rich HTML page has no plain text to pull out and will not import, so save it yourself and upload it instead.

## Reading progress

Progress is recorded per user, per document, as a scroll fraction between 0 and 1 plus the last page for paged formats. It is what drives the progress bar on the document, and it is stored server-side rather than in the browser, so picking a guide back up on your phone lands where you left it on your desktop.

Progress is per document, not per game, so two guides for the same game track separately.

## API

| Method   | Path                                      | Description                                     |
| -------- | ----------------------------------------- | ----------------------------------------------- |
| `POST`   | `/roms/{id}/walkthroughs/files`           | Upload a walkthrough document                   |
| `POST`   | `/roms/{id}/walkthroughs/gamefaqs`        | Import one from a GameFAQs URL, as plain text   |
| `DELETE` | `/roms/{id}/walkthroughs/files/{file_id}` | Delete a walkthrough                            |
| `GET`    | `/roms/{rom_id}/files/{file_id}/progress` | The requester's reading progress for a document |
| `PUT`    | `/roms/{rom_id}/files/{file_id}/progress` | Record reading progress                         |

The upload endpoint streams the body and takes the filename in an `x-upload-filename` header, with optional `x-doc-title` and `x-doc-author` headers. The progress endpoints are per user, so they need no user id and cannot read anyone else's position.

## Related

- [Folder Structure](../getting-started/folder-structure.md#multi-file-games): the other subfolders a game folder can carry
- [Uploads](uploads.md): how files reach the library
