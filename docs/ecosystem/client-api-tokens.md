---
title: Client API Tokens
description: Long-lived bearer tokens for companion apps, plus the device-pairing flow.
---

# Client API Tokens

A **Client API Token** is a long-lived credential that a companion app (or script, or CI job) uses to authenticate against RomM on behalf of a specific user. Think "personal access token" on GitHub.

Tokens are **per-user** and **per-scope-subset**: a token can hold any subset of the owning user's scopes, scoped narrower than the user's role. You get up to **25 active tokens per user**.

## Why not just store a password?

- Passwords grant full access to the account; tokens can be scope-narrowed.
- Tokens are one-click revocable without changing your password.
- Tokens are safer to type (or paste) into a companion app's config file than a password.
- Tokens can be bound to a single device via the pairing flow, avoiding typing them at all.

## Token format

40 hex characters prefixed with `rmm_`:

```text
rmm_abcdef0123456789abcdef0123456789abcdef01
```

Send as a bearer token on any authenticated API call:

```http
Authorization: Bearer rmm_abcdef...
```

## Creating a token

From the RomM UI: **Profile → Client API Tokens → + New Token**.

- **Name**: descriptive (e.g. "Grout on RG35XX").
- **Scopes**: tick which scopes to include. Default: read-only. Think about it; don't give every token `users.write`.
- **Expiry**: optional; blank = never expires until revoked.

The token is shown **exactly once**. Copy it now. If you lose it, revoke and regenerate; you can't get it back.

## Device pairing (short-code flow)

Typing a 44-character token into a handheld thumbstick isn't realistic. Instead:

### Flow

```
┌───────────┐                                 ┌───────────┐
│  Device   │                                 │   RomM    │
└─────┬─────┘                                 └─────┬─────┘
      │                                             │
      │ 1. POST /api/client-tokens/{id}/pair        │
      │ (from the web UI, by the token's owner)     │
      │<── generates short code (8 digits) ─────────│
      │                                             │
      │ 2. Device user types the 8-digit code       │
      │    into the companion app                   │
      │                                             │
      │ 3. Device: POST /api/client-tokens/exchange │
      │     body: { "code": "12345678" }            │
      │──────────────────────────────────────────→  │
      │                                             │
      │<── full token (rmm_...) ────────────────────│
      │                                             │
      │ 4. Device stores the token, uses it from    │
      │    now on.                                  │
      │                                             │
```

### Timing

- Pairing codes are valid for **5 minutes** after creation.
- Single-use: once a device exchanges the code, it's invalid for anyone else.
- Re-create if the user doesn't complete within the window.

### Who generates the code

The user who owns the token, from a device already signed into RomM (web UI, usually). The handheld / companion device then enters the code. No way for a device to generate a code on its own; that would defeat the pairing.

### What "pairing" gives you

A Client API Token bound to the device's installation. The companion app stores the token and uses it on every subsequent API call. From RomM's side, it looks like any other token: no special treatment beyond the fact that pairing is how the token got there.

## API reference for implementers

All the endpoints a companion app needs:

### Claim an outstanding pairing code (device-side)

```http
POST /api/client-tokens/exchange
Content-Type: application/json

{ "code": "12345678" }
```

Response:

```json
{
  "id": 42,
  "name": "Grout on RG35XX",
  "token": "rmm_abcdef0123456789abcdef0123456789abcdef01",
  "scopes": ["roms.read", "platforms.read", "assets.read", "assets.write"],
  "expires_at": null
}
```

If the code is invalid / expired / already used, returns 401.

### Generate a pairing code (server-side, called from the UI)

```http
POST /api/client-tokens/{id}/pair
Authorization: Bearer <session cookie or token>
```

Requires the caller own the token. Response includes the short code.

### Check pairing status (device-side, polling)

```http
GET /api/client-tokens/pair/{code}/status
```

Returns whether the code has been claimed, expired, or is still waiting. Poll every few seconds from the device side if you want instant feedback.

### Token lifecycle

```http
POST   /api/client-tokens             # create (from UI)
GET    /api/client-tokens             # list own tokens
DELETE /api/client-tokens/{id}        # revoke
PUT    /api/client-tokens/{id}/regenerate   # new secret, same scopes
```

Admin-only:

```http
GET    /api/client-tokens/all         # list every token on the server
DELETE /api/client-tokens/{id}/admin  # revoke any user's token
```

## Scoping tokens properly

A token can only hold scopes the owning user *also* holds. If the user is an Editor, their token can hold any Editor scope, but not `users.write` (which is Admin-only).

Useful narrow scope-sets:

- **Library-only read**: `roms.read`, `platforms.read`, `collections.read`, `devices.read` (e.g. for a browse-only app).
- **Read + sync saves**: add `assets.read`, `assets.write`, `me.read`, `me.write`, `devices.write`.
- **Playnite / external launcher**: `roms.read`, `platforms.read`, `collections.read` (it only needs to browse and download).
- **Grout / handheld companion**: library-read + assets read/write + device management.

The UI's scope-selection step defaults to read-only. Only tick write scopes you actually need.

## What happens on user role change

If the owning user's role drops below what the token needs:

- Token continues to exist but fails at request time with **403 Forbidden**.
- RomM doesn't automatically revoke it; that's the user's decision.

If the user is deleted, all their tokens are revoked immediately.

## Anti-patterns

- **Sharing a token between users.** Tokens are single-user. If two people need access, give them each an account and each creates their own token.
- **Embedding a token in public source.** Obvious but worth saying. If you accidentally commit one, revoke immediately from the RomM UI.
- **A single token for every app.** Name and scope per-app; revoking one doesn't kill the others.
- **Infinite-expiry tokens in untrusted locations.** If a device might be lost / handed off, set an expiry.

## See also

- [Device Sync Protocol](device-sync-protocol.md): how the synced content flows after pairing.
- [API Authentication](../developers/api-authentication.md): all RomM auth modes side-by-side.
- [Users & Roles → scope matrix](../administration/users-and-roles.md#scope-matrix): the 19-scope taxonomy.
