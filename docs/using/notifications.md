---
title: Notifications
description: Your notification inbox, and forwarding it to webhooks, email and chat services
---

# Notifications

Each user has a notification inbox at `/notifications`. It stores each one and then pushes it to every tab you have open, so one that arrives while you're away is still there the next time you sign in. The inbox keeps your 200 newest notifications, and you can mark them read or dismiss them one at a time or all at once.

## What sends a notification

| Event                                                       | Level           | Who gets it                                                                                                          | Topic       |
| ----------------------------------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------- | ----------- |
| A scan finished                                             | success         | Whoever started it. A scheduled or watcher scan notifies every admin, but only when it found new games or platforms. | `scans`     |
| A scan failed                                               | error           | Whoever started it, or every admin for a scheduled or watcher scan                                                   | `scans`     |
| A task finished                                             | success         | Whoever ran it by hand. Scheduled runs that succeed stay quiet.                                                      | `tasks`     |
| A task failed                                               | error           | Whoever ran it, or every admin for a scheduled run                                                                   | `tasks`     |
| Someone else ended your streaming session                   | warning         | The user whose stream was ended                                                                                      | `streaming` |
| Your role changed                                           | info            | The user whose role an admin changed                                                                                 | `account`   |
| One of your channels was turned off                         | warning         | The channel's owner, after 10 failed deliveries in a row                                                             | `account`   |
| A game was installed on one of your devices, or couldn't be | success / error | The user who sent the [install request](devices.md)                                                                  | `devices`   |
| A notification sent through the API                         | any             | The recipients the sender named (see [Sending notifications](#sending-notifications))                                | `custom`    |

A notification caused by another user, such as a role change or an ended stream, names that user as its sender.

## Channels

A channel forwards your notifications somewhere outside RomM. Each user sets up their own, up to 20, and each channel has two filters:

- **Minimum level**: `info` forwards everything, `warning` forwards warnings and errors, and `error` forwards errors only, with success notifications counting as `info`.
- **Topics**: any of `scans`, `tasks`, `streaming`, `devices`, `account` and `custom`, or all of them (the default).

A background worker delivers to channels, so a slow destination doesn't hold up RomM. A failed delivery is retried after 30 seconds, 2 minutes and 10 minutes. After 10 failed deliveries in a row the channel turns itself off and you get a notification saying why, with the last error kept on the channel. Any channel can send a test notification on demand, which reports the destination's error right away and isn't retried.

Text that leaves RomM is in English, whatever language the UI is set to. When [`ROMM_BASE_URL`](../reference/environment-variables.md) points at a real host (not `localhost` or a loopback address), messages carry an absolute link back to the page the notification is about.

Channel settings, including webhook URLs, secrets and service tokens, are encrypted with `ROMM_AUTH_SECRET_KEY`. Changing that key leaves existing channels unreadable, so they have to be set up again.

### Webhook

A webhook channel `POST`s RomM's own JSON to a URL you give it:

```json
{
    "event": "notification",
    "id": 1234,
    "kind": "scan_completed",
    "level": "success",
    "title": "Scan completed",
    "body": "12 new games",
    "url": "https://romm.example.com/scan",
    "data": {
        "scanned_roms": 340,
        "new_roms": 12,
        "identified_roms": 11,
        "new_platforms": 0
    },
    "actor": null,
    "created_at": "2026-10-05T09:12:44.512000+00:00"
}
```

- `kind` is one of `scan_completed`, `scan_failed`, `task_completed`, `task_failed`, `streaming_session_ended`, `role_changed`, `channel_disabled`, `device_install_completed` and `device_install_failed`, or `custom` (or a client's own kind) for a notification sent through the API.
- `title` and `body` are rendered English text, and `data` holds the raw values they were built from (a scan's `data` carries all of its counts, trimmed in the example above).
- `url` is `null` when `ROMM_BASE_URL` doesn't point anywhere shareable.
- `actor` is `{"id": ..., "username": ...}` when another user caused the notification, otherwise `null`.

The request has `Content-Type: application/json` and `User-Agent: RomM`, and must answer with a 2xx within 15 seconds. Redirects aren't followed, so a `3xx` counts as a failure.

Only an admin's webhook may point at a private or local address (`192.168.x.x`, `10.x.x.x`, a container name, and so on), so other users' webhooks are limited to public hosts.

#### Verifying the signature

Give the channel a secret, and every request carries an `X-RomM-Signature` header holding `sha256=` followed by the hex HMAC-SHA256 of the raw request body, keyed with that secret. Compute the same digest over the body exactly as received (before parsing the JSON) and compare the two in constant time:

```python
import hashlib
import hmac


def is_from_romm(secret: str, body: bytes, header: str | None) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return header is not None and hmac.compare_digest(expected, header)
```

### Email

Each notification arrives as a plain-text message whose subject starts with `[RomM]`. This channel is only offered once the server has [email set up](../administration/email.md).

A new address first receives a 6-digit confirmation code, which you enter to confirm the channel. The code expires after 30 minutes and allows 5 tries, and a new one can be requested after a minute. Changing a channel's address asks for a new confirmation.

### Apprise

Admins can also forward notifications to any service [Apprise](https://github.com/caronc/apprise) supports, such as Discord, Telegram, Slack, ntfy, Gotify, Matrix, Pushover or Microsoft Teams. A channel takes the service's fields, or the service's own URL (a Discord webhook URL, for example) or an Apprise URL, which is split into those fields. Each service links to its setup guide on the [Apprise wiki](https://github.com/caronc/apprise/wiki).

Apprise channels are admin-only because Apprise opens its own connections, which could otherwise be pointed at the local network. Services that act on the machine running RomM (desktop notifications, syslog, D-Bus and the like) aren't offered.

## Sending notifications

Anyone can send a notification to themselves, so scripts and companion apps can report back. Admins can also send one to other users, to every admin or to everyone, and the recipients see the admin as its sender.

```sh
curl -X POST https://romm.example.com/api/notifications \
  -H "Authorization: Bearer $ROMM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Nightly backup finished",
        "body": "Saves and states were copied to the NAS.",
        "level": "success",
        "kind": "backup.done",
        "link": "/settings",
        "icon": "mdi-backup-restore",
        "recipients": "admins"
      }'
```

| Field        | Required | Description                                                                                                                                         |
| ------------ | :------: | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`      |   yes    | Up to 255 characters                                                                                                                                |
| `body`       |          | Up to 1000 characters                                                                                                                               |
| `level`      |          | `info` (default), `success`, `warning` or `error`                                                                                                   |
| `kind`       |          | Your own identifier, such as `argosy.sync_done` (lowercase letters, digits and `_ . : -`). Defaults to `custom`, and RomM's own kinds are reserved. |
| `link`       |          | A path inside RomM, such as `/rom/12`. External URLs are refused.                                                                                   |
| `icon`       |          | A [Material Design Icons](https://pictogrammers.com/library/mdi/) name, such as `mdi-sync`                                                          |
| `data`       |          | Any JSON object up to 4096 characters, forwarded as-is in webhook payloads                                                                          |
| `recipients` |          | `null` (yourself, the default), a list of user ids, `"admins"` or `"all"`. Anything but yourself needs an admin with the `users.write` scope.       |

The response is the list of notifications created, one per recipient, each in the `custom` topic that channels filter by. Disabled users are skipped when sending to `admins` or `all`, and naming a missing or disabled user by id returns `404`.

## API

| Method | Path                                                  | Scope      | Description                                                    |
| ------ | ----------------------------------------------------- | ---------- | -------------------------------------------------------------- |
| GET    | `/api/notifications`                                  | `me.read`  | Your notifications, newest first                               |
| POST   | `/api/notifications`                                  | `me.write` | Send a notification (`users.write` too for other recipients)   |
| POST   | `/api/notifications/read`                             | `me.write` | Mark the given `ids` read, or all of them when `ids` is `null` |
| DELETE | `/api/notifications/{notification_id}`                | `me.write` | Dismiss one notification                                       |
| DELETE | `/api/notifications`                                  | `me.write` | Dismiss all your notifications                                 |
| GET    | `/api/notification-channels`                          | `me.read`  | Your channels                                                  |
| POST   | `/api/notification-channels`                          | `me.write` | Add a channel (an email address is sent a confirmation code)   |
| PATCH  | `/api/notification-channels/{channel_id}`             | `me.write` | Change a channel                                               |
| DELETE | `/api/notification-channels/{channel_id}`             | `me.write` | Delete a channel                                               |
| POST   | `/api/notification-channels/{channel_id}/test`        | `me.write` | Send a test notification now                                   |
| POST   | `/api/notification-channels/{channel_id}/confirm`     | `me.write` | Confirm an email channel with its `code`                       |
| POST   | `/api/notification-channels/{channel_id}/resend-code` | `me.write` | Email a new confirmation code                                  |
| GET    | `/api/notification-channels/apprise-services`         | `me.read`  | Every Apprise service and its fields (admins only)             |
| POST   | `/api/notification-channels/apprise-services/parse`   | `me.read`  | Read a service URL or Apprise URL into fields (admins only)    |

Open tabs hear about changes over the `notifications:new`, `notifications:read` and `notifications:dismissed` socket events (see [WebSockets](../developers/websockets.md)).
