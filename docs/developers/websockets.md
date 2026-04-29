---
title: WebSockets
description: Endpoints for live updates
---

<!-- trunk-ignore-all(markdownlint/MD024) -->

# WebSockets

RomM uses **socket.io** for real-time communication, with two endpoints serving distinct purposes:

| Endpoint             | Purpose                                                                       |
| -------------------- | ----------------------------------------------------------------------------- |
| `/ws/socket.io`      | Live updates (scan progress, task status, ROM mutations, admin notifications) |
| `/netplay/socket.io` | Netplay session coordination (room discovery, join/leave, lifecycle)           |

## Authentication

socket.io connections inherit the HTTP session, so if your `Cookie` header carries a session cookie, the WebSocket connection authenticates as that user. Programmatic clients pass the credential via the handshake `auth` field:

```javascript
const socket = io("https://demo.romm.app", {
    path: "/ws/socket.io",
    auth: {
        token: "rmm_...",
    },
});
```

A failed handshake closes the connection with an error event.

## Reverse-proxy requirements

Every reverse-proxy setup must forward the WebSocket upgrade. The recipes in [Reverse Proxy](../install/reverse-proxy.md) all keep WebSockets on by default.

Common breakages:

- Nginx without `proxy_set_header Upgrade $http_upgrade` and `Connection "upgrade"`
- Cloudflare with WebSockets disabled in Network settings
- Traefik without the default passthrough middlewares

A broken WS typically shows up as HTTP 400 on the upgrade request plus a flood of `WebSocket connection failed` errors in the browser console. [Authentication Troubleshooting → WebSockets](../troubleshooting/authentication.md#400-bad-request-on-the-websocket-endpoint) covers the diagnosis.
