# Multiplayer Netplay Setup

RomM supports **multiplayer netplay** using EmulatorJS: play retro games with friends remotely in real time. This guide covers setting up **SFU-based netplay**, which uses a dedicated mediasoup server for reliable audio, video, and input relay. It is a self hosted dedicated netplay server. This approach scales better than peer-to-peer for multiple players and spectators.

## Overview

- **4 Player Lobbies**: One player hosts, the other joins via the netplay menu, and livestream video/audio, while streaming their own inputs to the host.
- **Spectators**: Additional viewers can watch the stream without controlling the game. The SFU server can support ~50-100 livestream users per worker.
- **Supported systems**: Same platforms as [EmulatorJS](Platforms-and-Players/EmulatorJS-Player.md); best for 2-player, co-op, turn-based, and party games. Video latency varies with network setups and host hardware. Streaming is optimized for low video latency but may not always feel playable for certain games with more action.
- **Dedicated Server**: The SFU is currently a self hosted server for your own personal romm domain. The server is fundamentally scalable, and I expect to introduce support for federated mesh networking to connect your romm domain with your trusted friend's domain explicitly for sharing lobby data and connecting over netplay.

## Requirements

- RomM full image (includes EmulatorJS-SFU assets) or a custom build with SFU support
- Docker or Podman
- The [romm-sfu](https://github.com/rommapp/romm-sfu-server) server image (mediasoup + Socket.IO)
- TURN/STUN servers for players behind strict NAT (see [ICE servers](#ice-servers)). A STUN/TURN is needed for reliable server connectivity, but TURN will rarely be used if the SFU is configured correctly unless players are behind strict firewalls.

## Quick setup with Docker Compose

### 1. Build or obtain the SFU image

The SFU server is built from the [romm-sfu-server](https://github.com/rommapp/romm-sfu-server) repository:

```bash
cd romm-sfu-server
docker build -t emulatorjs-sfu:latest .
```

Or use a pre-built image if one is published for your architecture.

### 2. Use a docker-compose stack with RomM + SFU

Create a `docker-compose.yml` that includes both RomM and the SFU service. The key requirement: **both containers share the same Docker network** so RomM can reach the SFU, and the SFU can call RomM's internal API.

You can also copy from the [RomM examples](https://github.com/rommapp/romm/blob/master/examples/docker-compose.example.yml).

### 3. Set required environment variables

| Variable                   | Where            | Description                                                                                              |
| -------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------- |
| `ROMM_AUTH_SECRET_KEY`     | RomM             | Generate with `openssl rand -hex 32`                                                                     |
| `ROMM_SFU_INTERNAL_SECRET` | RomM **and** SFU | Shared secret for SFU ↔ RomM API. Generate with `openssl rand -hex 32` — **must match in both services** |
| `SFU_HOST`                 | RomM             | Hostname of the SFU. Use the Docker service name (e.g. `romm-sfu`) when both run in the same stack       |
| `SFU_PORT`                 | RomM             | SFU HTTP/WS port (default `3001`)                                                                        |
| `ROMM_API_BASE_URL`        | SFU              | URL RomM is reachable at from the SFU (e.g. `http://romm:8080` inside Docker)                            |

### 4. Enable netplay via config or environment

Enable netplay either in RomM config (e.g. `/romm/config/config.yml`):

```yaml
emulatorjs:
  netplay:
    enabled: true
```

Or via environment variable (overrides config):

```yaml
SFU_NETPLAY_ENABLED=true
```

When `SFU_NETPLAY_ENABLED=true`, RomM loads EmulatorJS-SFU from jsDelivr. When `false`, it uses the original EmulatorJS from cdn.emulatorjs.org (no netplay).

### 5. Expose required ports

- **RomM**: `8080` (or your chosen port)
- **SFU**: `3001` (TCP), `20000` (WebRTC UDP/TCP) — adjust if using `USE_WEBRTC_SERVER=1` with multiple workers (below).
- **SFU**: More WebRTC ports are required if you use multiple SFU workers (below)

For internet play, ensure these ports are reachable (firewall, reverse proxy) and consider [host networking](#host-networking-linux) for the SFU on Linux.

## ICE servers

For players behind strict NAT or symmetric firewalls, configure TURN/STUN servers in `config.yml`:

```yaml
emulatorjs:
  netplay:
    enabled: true
    ice_servers:
      - urls: "stun:stun.l.google.com:19302"
      - urls: "turn:openrelay.metered.ca:80"
        username: "openrelayproject"
        credential: "openrelayproject"
```

NOTE: You must enter your STUN/TURN server settings in the config.yml under emulatorjs here, but also you will see you need to include them under the romm-sfu container environment variables in docker-compose.yml. The reason is to allow support in the future for you to set a "home ICE server config" while allowing you to use ICE servers preferred by the SFU server, if for example, you are roaming, and connect to an SFU node in the mesh hosted by your friend, then you can use their ICE servers once you've negotiated a connection with the SFU. This allows optimal routing as networks get more advanced.

A free-tier [Metered](https://www.metered.ca/stun-turn) account gives you dedicated TURN credentials for better reliability.

## Playing a game

1. Start a game in EmulatorJS.
2. Click the 🌐 icon in the bottom bar.
3. Enter your name (or Netplay ID if configured).
4. **Host**: Create a room (password optional).
5. **Join**: Select the room from the list and join.
6. All players must have access to your RomM instance to connect.

## Advanced options

### Host networking (Linux)

For best WebRTC performance when clients connect over the public internet, run the SFU with `network_mode: host`:

```yaml
romm-sfu:
  image: emulatorjs-sfu:latest
  network_mode: host
  environment:
    - PORT=3001
    - WEBRTC_PORT=20000
    - ANNOUNCED_IP=your-public-ip-or-hostname
    - ROMM_API_BASE_URL=http://127.0.0.1:8080 # RomM on host
    - ROMM_SFU_INTERNAL_SECRET=${ROMM_SFU_INTERNAL_SECRET}
```

Then set `SFU_HOST=host.docker.internal` (or `host.containers.internal` on Podman) in RomM so it can reach the SFU on the host.

NOTE: The SFU relay server is a WebRTC application, and despite any optimizations I can make with nodejs and mediasoup, WebRTC semantics still require ICE negotiations which have a very large, randomly employed ephemeral range. I cannot support performance or stability optimization on setups with hundreds or thousands of webrtc ports forwarded in docker emulation to support ICE which consumes a lot of resources and overhead, even if it can be forced to work. It is for this reason that I cannot offer a solution for standard bridged container networking on the host machine.

### SFU on a separate host

If the SFU runs elsewhere (different machine or data center):

- Set `SFU_HOST` and `SFU_PORT` in RomM to that host.
- Set `ROMM_API_BASE_URL` in the SFU to the public URL of RomM (e.g. `https://romm.example.com`).
- Set `ANNOUNCED_IP` to the domain name or public IP address of the machine hosting your SFU server node.
- Ensure the SFU can reach RomM’s internal API and that RomM can reach the SFU. You can verify with `docker logs romm-sfu`

### Multiple SFU workers

For high concurrency, run multiple mediasoup workers. Each worker should probably support about 100 users, and so on a gigabit connection with 2 cores, given the low bitrate streams employed by netplay, you can support about max 200 users at 720p 60fps across any number of active lobbies.

```yaml
romm-sfu:
  environment:
    - USE_WEBRTC_SERVER=1
    - SFU_WORKER_COUNT=2
    - WEBRTC_PORT=20000
```

`USE_WEBRTC_SERVER=1` is required when `SFU_WORKER_COUNT > 1`. Here is why:

Each worker requires it's own dedicated port open on the docker container (unless you use network mode `host`).

`WEBRTC_PORT` value determines the initial port # for the first worker, and each other worker incrementally takes the next port.

Under standard webrtc semantics, each worker might require _hundreds_ of ports dedicated to itself, but `USE_WEBRTC_SERVER=1` enables routing them all through a single port. Even then, each worker needs it's own dedicated port.

You must have `WEBRTC_PORT=20000` set, and it should use a very high port number. You also must open multiple ports per worker, incrementally. **For example:** If `WEBRTC_PORT=20000` and `SFU_WORKER_COUNT=4` then you must open UDP (and optionally TCP, for TLS TURNS users) on ports 20000, 20001, 20002, and 20003. One for each CPU worker.

Only the SFU server needs to be aware of what the `WEBRTC_PORT` is set to, because sessions are initiated over port 3001 and the SFU server assigns webrtc ports on initialization of the sessions.

If you do use multiple workers, you can also optionally enable experimental feature `SFU_FANOUT_ENABLED=1` to support load balancing on the SFU server that enables the ability to balance lobbies that are so large from spectator count, that you span the load for a single lobby across multiple workers.

## Environment variables reference

See [Environment Variables](Environment-Variables.md) for the full list. Key ones for netplay:

| Variable                                      | Service   | Description                                                                                                                                           |
| --------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ROMM_SFU_INTERNAL_SECRET`                    | RomM, SFU | Shared secret for SFU → RomM auth (required for netplay user authentication)                                                                          |
| `SFU_HOST`                                    | RomM      | SFU Hostname (Suggest `host.docker.internal` or `host.containers.internal` on podman, for SFU nodes with host networking on the same machine as romm) |
| `SFU_PORT`                                    | RomM      | SFU server TCP port (default `3001`)                                                                                                                  |
| `EMULATORJS_SFU_HOST` / `EMULATORJS_SFU_PORT` | RomM      | Alternative names for SFU_HOST/SFU_PORT                                                                                                               |
| `ANNOUNCED_IP`                                | SFU       | Node specific, must match node's public address                                                                                                       |
| `LISTEN_IP`                                   | SFU       | Listen on any IP (0.0.0.0) or restrict to specific IP                                                                                                 |
| `PUBLIC_URL`                                  | SFU       | Report what network SFU belongs to for other nodes                                                                                                    |
| `PORT`                                        | SFU       | SFU port for standard requests. Must be forwarded.                                                                                                    |
| `ENABLE_WEBRTC_TCP`                           | SFU       | Allow advanced TCP TURN/S negotiation over port 80/443 that get rerouted to the TURN server over proxy to bypass advanced firewalls.                  |
| `SFU_FANOUT_ENABLED`                          | SFU       | SFU worker support lobbies that span multiple workers                                                                                                 |
| `SFU_WORKER_COUNT`                            | SFU       | SFU workers request dedicated use of a CPU core, "pin" CPU cores in the kernel to optimize worker performance.                                        |
| `USE_WEBRTC_SERVER`                           | SFU       | Route WebRTC traffic through a single port.                                                                                                           |
| `ROMM_API_BASE_URL`                           | SFU       | Base URL for API calls required for user authentication and other features.                                                                           |
| `SFU_STUN_SERVERS`                            | SFU       | A comma delimited list of stun server details.                                                                                                        |
| `SFU_TURN_SERVERS`                            | SFU       | A list of dict formatted objects to store TURN credentials.                                                                                           |
| `LOG_LEVEL`                                   | SFU       | Set to `debug` for verbose logging.                                                                                                                   |

### Split Horizon Networking

To acheive high performance results on your local network, while still being reachable to the outside, instead of setting your `ANNOUNCED_IP` on the SFU to a local LAN IP, set it to a domain name that your external users can reach (like the domain of romm if hosted on the same network) and use a private DNS service on your own local network to rewrite DNS requests for your own local romm or SFU server's domain name to the local LAN IP of your server. This intercepts local network DNS request for the IP of romm-sfu.coolguy.net, and gives the local LAN IP for optimal routing for local networks and VPN users. Setting this to a domain or IP that isn't publicly reachable effectively prevents outside users from accessing the SFU for netplay.

## Troubleshooting

- **404 on loader.js or mediasoup-client-umd.js**: With SFU netplay enabled, EmulatorJS-SFU and mediasoup are loaded from jsDelivr CDN by default. If mediasoup fails from CDN, RomM falls back to `/assets/emulatorjs-sfu/data/vendor/` (requires RomM full image). The slim image does not include EmulatorJS-SFU assets.
- **Connection refused to SFU**: Check `SFU_HOST` and `SFU_PORT`, and that both services share a Docker network (or use `host.docker.internal` for host-mode SFU).
- **Token/auth errors**: Ensure `ROMM_SFU_INTERNAL_SECRET` is identical in RomM and the SFU.
- **WebRTC fails behind NAT**: Add TURN servers in `config.yml` under `emulatorjs.netplay.ice_servers`.
