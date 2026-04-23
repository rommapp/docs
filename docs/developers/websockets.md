---
title: WebSockets
description: RomM's two Socket.IO endpoints for live updates and Netplay coordination.
---

<!-- trunk-ignore-all(markdownlint/MD024) -->

# WebSockets

RomM uses **Socket.IO** for real-time communication. Two endpoints:

| Endpoint             | Purpose                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------- |
| `/ws/socket.io`      | General live updates: scan progress, task status, task completion, admin notifications. |
| `/netplay/socket.io` | Netplay session coordination: room discovery, join/leave events, session lifecycle.     |

Both are Redis-backed (via `socket.io-redis`) so multi-instance RomM deployments broadcast events to every replica.

## Why Socket.IO not raw WebSocket?

RomM inherited Socket.IO from the Vue frontend, which uses `socket.io-client`. Sticking with Socket.IO avoids protocol drift, works in every browser, and handles reconnection + message framing for us.

If you're writing a non-browser client in a language that has a Socket.IO library (Python's `python-socketio`, Go's `go-socket.io`, etc.), the protocol is straightforward. Raw WebSocket without Socket.IO framing **will not** work, because Socket.IO adds its own handshake and message envelope.

## Authentication

Socket.IO connections inherit the HTTP session: if your `Cookie` header carries a RomM session cookie, the WS connection is authenticated as that user. Programmatic clients should pass the session or token via the handshake `auth` field:

```javascript
const socket = io("https://romm.example.com", {
    path: "/ws/socket.io",
    auth: {
        token: "rmm_...",
    },
});
```

If auth fails, the connection is closed with an error event.

## `/ws/socket.io`: general events

### Server → client events

| Event           | Payload                                            | When                                    |
| --------------- | -------------------------------------------------- | --------------------------------------- |
| `scan:start`    | `{ scan_id, platforms, mode }`                     | A scan starts.                          |
| `scan:log`      | `{ scan_id, level, message }`                      | Live scan log line.                     |
| `scan:progress` | `{ scan_id, platform, matched, unmatched, total }` | Per-platform progress update.           |
| `scan:complete` | `{ scan_id, summary }`                             | Scan finished.                          |
| `task:start`    | `{ task_id, task_name }`                           | Any scheduled/manual task starts.       |
| `task:complete` | `{ task_id, task_name, status }`                   | Task finished (status: success/failed). |
| `rom:created`   | `{ rom_id }`                                       | New ROM added.                          |
| `rom:updated`   | `{ rom_id }`                                       | Metadata or user data changed.          |
| `rom:deleted`   | `{ rom_id }`                                       | ROM removed.                            |
| `notification`  | `{ message, level }`                               | Admin broadcast / error message.        |

### Client → server events

No state changes via WebSocket. RomM's design is "REST for writes, Socket.IO for reads". A client can:

- Emit `subscribe:scan` with a scan ID to join that scan's broadcast group.
- Emit `unsubscribe:scan` to leave.

Actual scan / task / ROM operations happen via the REST API. See [API Reference](api-reference.md).

## `/netplay/socket.io`: Netplay coordination

Separate endpoint for Netplay rooms. Used by EmulatorJS's Netplay logic, rarely touched directly.

### Server → client events

| Event                    | Payload                                         |
| ------------------------ | ----------------------------------------------- |
| `netplay:room_created`   | `{ room_id, host, rom_id, password_protected }` |
| `netplay:room_updated`   | `{ room_id, players }`                          |
| `netplay:room_destroyed` | `{ room_id }`                                   |

### Client → server events

| Event                 | Payload                              |
| --------------------- | ------------------------------------ |
| `netplay:create_room` | `{ rom_id, password?, max_players }` |
| `netplay:join_room`   | `{ room_id, password? }`             |
| `netplay:leave_room`  | `{ room_id }`                        |

Plus WebRTC signalling events (`offer`, `answer`, `ice_candidate`) that shuttle between peers for the actual game session. These are opaque to anything but EmulatorJS.

## Redis backend (multi-instance)

When you run multiple RomM replicas behind a load balancer, a WS-originated event on one replica needs to reach a client connected to another replica. `socket.io-redis` handles that: events are published to a Redis pub/sub channel, every replica subscribes, every replica delivers to its local sticky-session clients.

Required config when running multi-replica:

- `REDIS_HOST` + `REDIS_PORT` shared across replicas
- Load balancer with **sticky sessions** (client IP or cookie hash)

Without sticky sessions, Socket.IO's handshake polling phase can bounce between replicas and fail. See [Socket.IO multi-server docs](https://socket.io/docs/v4/using-multiple-nodes/) for context.

## Reverse-proxy requirements

Every reverse-proxy setup must forward the WebSocket upgrade. See [Reverse Proxy](../install/reverse-proxy.md). All recipes there keep WebSockets on.

Common breakages:

- Nginx without `proxy_set_header Upgrade $http_upgrade` / `Connection "upgrade"`
- Cloudflare with WebSockets off in Network settings
- Traefik without the default passthrough middlewares

Symptom of a broken WS: HTTP 400 responses on the upgrade, and the browser console full of `WebSocket connection failed`. See [Authentication Troubleshooting → WebSockets](../troubleshooting/authentication.md#400-bad-request-on-the-websocket-endpoint).

## Writing a client in Python

Simple example, tail scan logs:

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
    "https://romm.example.com",
    socketio_path="/ws/socket.io",
    auth={"token": "rmm_..."},
)
sio.wait()
```

## Limitations

- **Not every backend action emits a WS event.** Only the ones listed above. If you need a specific event, open an issue.
- **No room-based user presence yet.** "Who else is online" isn't exposed.
- **Netplay WebRTC is peer-to-peer after initial handshake.** RomM only brokers. The actual gameplay data never touches RomM's servers.

## See also

- [API Authentication](api-authentication.md): general auth primer
- [Reverse Proxy](../install/reverse-proxy.md): every recipe needs WebSocket passthrough.
- [Netplay](../using/netplay.md): end-user-facing side of the `/netplay` endpoint
