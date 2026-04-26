---
title: WebSockets
description: RomM's two Socket.IO endpoints for live updates and Netplay coordination
---

<!-- trunk-ignore-all(markdownlint/MD024) -->

# WebSockets

RomM uses **Socket.IO** for real-time communication, with two endpoints serving distinct purposes:

| Endpoint             | Purpose                                                                       |
| -------------------- | ----------------------------------------------------------------------------- |
| `/ws/socket.io`      | Live updates: scan progress, task status, ROM mutations, admin notifications  |
| `/netplay/socket.io` | Netplay session coordination: room discovery, join/leave, lifecycle           |

Both are Valkey-backed via `socket.io-redis`, which means multi-instance deployments fan events out to every replica without you having to wire that up yourself.

## Why Socket.IO not raw WebSocket?

RomM inherited Socket.IO from the Vue frontend (which uses `socket.io-client`), and sticking with it avoids protocol drift, keeps things working in every browser, and gets us reconnection and message framing for free.

If you're writing a non-browser client in a language with a Socket.IO library (Python's `python-socketio`, Go's `go-socket.io`, etc.), the protocol is straightforward. **Raw WebSocket without Socket.IO framing will not work**, because Socket.IO adds its own handshake and message envelope on top.

## Authentication

Socket.IO connections inherit the HTTP session: if your `Cookie` header carries a RomM session cookie, the WebSocket connection authenticates as that user. Programmatic clients pass the credential via the handshake `auth` field:

```javascript
const socket = io("https://demo.romm.app", {
    path: "/ws/socket.io",
    auth: {
        token: "rmm_...",
    },
});
```

A failed handshake closes the connection with an error event.

## `/ws/socket.io`: general events

### Server → client

| Event           | Payload                                            | When                                  |
| --------------- | -------------------------------------------------- | ------------------------------------- |
| `scan:start`    | `{ scan_id, platforms, mode }`                     | A scan starts                         |
| `scan:log`      | `{ scan_id, level, message }`                      | Live scan log line                    |
| `scan:progress` | `{ scan_id, platform, matched, unmatched, total }` | Per-platform progress update          |
| `scan:complete` | `{ scan_id, summary }`                             | Scan finished                         |
| `task:start`    | `{ task_id, task_name }`                           | Any scheduled or manual task starts   |
| `task:complete` | `{ task_id, task_name, status }`                   | Task finished (success or failed)     |
| `rom:created`   | `{ rom_id }`                                       | New ROM added                         |
| `rom:updated`   | `{ rom_id }`                                       | Metadata or user data changed         |
| `rom:deleted`   | `{ rom_id }`                                       | ROM removed                           |
| `notification`  | `{ message, level }`                               | Admin broadcast or error message      |

### Client → server

State changes don't happen over the WebSocket. RomM's design is "REST for writes, Socket.IO for reads". A client can:

- Emit `subscribe:scan` with a scan ID to join that scan's broadcast group
- Emit `unsubscribe:scan` to leave

Actual scan, task, and ROM operations go through the REST API. See [API Reference](api-reference.md).

## `/netplay/socket.io`: Netplay coordination

A separate endpoint dedicated to Netplay rooms, driven by EmulatorJS's Netplay logic and rarely touched directly outside of it.

### Server → client

| Event                    | Payload                                         |
| ------------------------ | ----------------------------------------------- |
| `netplay:room_created`   | `{ room_id, host, rom_id, password_protected }` |
| `netplay:room_updated`   | `{ room_id, players }`                          |
| `netplay:room_destroyed` | `{ room_id }`                                   |

### Client → server

| Event                 | Payload                              |
| --------------------- | ------------------------------------ |
| `netplay:create_room` | `{ rom_id, password?, max_players }` |
| `netplay:join_room`   | `{ room_id, password? }`             |
| `netplay:leave_room`  | `{ room_id }`                        |

Plus WebRTC signalling events (`offer`, `answer`, `ice_candidate`) shuttling between peers for the actual game session. These are opaque to anything but EmulatorJS.

## Multi-replica deployments

When you run multiple RomM replicas behind a load balancer, an event originating on one replica needs to reach a client connected to another. `socket.io-redis` handles that by publishing events to a Valkey pub/sub channel and letting every replica deliver to its locally-connected clients.

Required when running multi-replica:

- `REDIS_HOST` + `REDIS_PORT` shared across replicas (Valkey works fine — it's Redis-compatible)
- A load balancer with **sticky sessions** (client-IP or cookie-hash routing)

Without sticky sessions, Socket.IO's handshake polling phase can bounce between replicas and fail. The [Socket.IO multi-server docs](https://socket.io/docs/v4/using-multiple-nodes/) cover the underlying mechanics.

## Reverse-proxy requirements

Every reverse-proxy setup must forward the WebSocket upgrade. The recipes in [Reverse Proxy](../install/reverse-proxy.md) all keep WebSockets on by default.

Common breakages:

- Nginx without `proxy_set_header Upgrade $http_upgrade` and `Connection "upgrade"`
- Cloudflare with WebSockets disabled in Network settings
- Traefik without the default passthrough middlewares

A broken WS typically shows up as HTTP 400 on the upgrade request plus a flood of `WebSocket connection failed` errors in the browser console — [Authentication Troubleshooting → WebSockets](../troubleshooting/authentication.md#400-bad-request-on-the-websocket-endpoint) covers the diagnosis.

## Writing a Python client

Tail scan logs from a script:

```python
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("connected")

@sio.on("scan:log")
def scan_log(data):
    print(f"[{data['level']}] {data['message']}")

sio.connect(
    "https://demo.romm.app",
    socketio_path="/ws/socket.io",
    auth={"token": "rmm_..."},
)
sio.wait()
```

## Limitations

- **Not every backend action emits an event.** Only the ones listed in the tables above — if you need a specific event for an integration, open an issue.
- **No room-based user presence yet.** "Who else is online" isn't exposed today.
- **Netplay is peer-to-peer after the initial handshake.** RomM only brokers the room, so the actual gameplay data never touches RomM's servers.
