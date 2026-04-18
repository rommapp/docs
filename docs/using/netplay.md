---
title: Netplay
description: Play EmulatorJS games with friends in real time: hosting, joining, ICE servers, and NAT.
---

# Netplay

**Netplay** lets you play [in-browser](in-browser-play.md) with other users in real time: co-op, turn-based, or party games, shared across the internet. EmulatorJS emulates "two players on one couch with two controllers", streaming video from the host to everyone else.

Best for 2-player co-op and turn-based games. Not ideal for twitchy fighting games (frame-level input isn't rollback-based).

!!! note "Netplay is a v5.0 feature"
    If you're on an older RomM (4.x), Netplay was disabled with known issues. 5.0 brings it back as a supported feature.

## Prerequisites

- EmulatorJS Netplay enabled in `config.yml` (operator-level).
- ICE servers configured (STUN + TURN); without them, Netplay only works when all players are on the same LAN.
- All players need access to your RomM instance. Netplay doesn't proxy the ROM to people without RomM accounts.

See [Configuration File → `emulatorjs.netplay`](../reference/configuration-file.md#emulatorjsnetplay-new-in-50) for the operator-side setup.

## Hosting a room

1. **Play** a supported game (any EmulatorJS platform works).
2. Once loaded, click the 🌐 (globe) icon in the bottom toolbar.
3. Enter your display name (shown to other players).
4. **Create Room** → optional password.
5. Players who can reach your RomM see the room in the Netplay list.

You're Player 1. Up to three more players can join as Players 2–4 (core-dependent; some only support 2).

## Joining a room

1. Open the same ROM (or any ROM, and open the 🌐 panel).
2. **Available Rooms** lists active rooms on your RomM.
3. Join → enter password if required.
4. Wait for the host to start. You'll see their game once the session's live.

Other players must be on **your RomM**. Netplay doesn't federate across instances.

## Controls

Every player controls their own gamepad / keyboard locally; inputs are sent to the host, which runs the game and broadcasts video. Slight lag is expected over the internet (~50–150 ms typical); higher on transatlantic hops or with TURN in the path.

## ICE servers (the NAT stuff)

WebRTC, the protocol Netplay uses, needs help to punch through consumer routers. That's what ICE (STUN + TURN) servers do:

- **STUN**: cheap; helps two peers find each other's public IPs. Works unless one of you is behind symmetric NAT.
- **TURN**: relays traffic when STUN can't. More resource-intensive; most free TURN services have quotas.

The operator wires ICE servers in `config.yml`:

```yaml
emulatorjs:
  netplay:
    enabled: true
    ice_servers:
      # Google's free public STUN, no account needed
      - urls: "stun:stun.l.google.com:19302"
      - urls: "stun:stun1.l.google.com:19302"
      # OpenRelay free TURN (rate-limited)
      - urls: "turn:openrelay.metered.ca:80"
        username: "openrelayproject"
        credential: "openrelayproject"
      - urls: "turn:openrelay.metered.ca:443"
        username: "openrelayproject"
        credential: "openrelayproject"
```

For production Netplay, operators should get a dedicated TURN account (free tier at [Metered](https://www.metered.ca/stun-turn), or self-host [coturn](https://github.com/coturn/coturn)).

## Limitations

- **Not all cores support Netplay.** SNES9x, Mupen64Plus, Mednafen PSX, Genesis Plus GX: generally yes. Cores like PPSSPP or dosbox-pure: no.
- **Frame-perfect fighting isn't realistic.** Netplay is for casual co-op, not tournament-level fighting games. Use something like [FightCade](https://www.fightcade.com/) for that.
- **All players need RomM access.** There's no "join a friend's game without an account"; guests need at least a Viewer account on your instance.
- **RTC over TURN uses real bandwidth.** Hosting a 4-player N64 session over TURN can saturate a modest uplink. Prefer STUN where possible.

## Known caveat: nightly CDN

When Netplay is enabled, EmulatorJS loads some assets (localisation, some cores) from the nightly CDN rather than the bundled stable assets.

```text
https://cdn.emulatorjs.org/nightly/...
```

Occasional hiccups (404s, untranslated UI strings) happen when the nightly is out of sync with the stable bundle RomM ships. Usually self-heals on the next RomM image update. If you care about long-term stability and don't need Netplay, leave it off.

## Security

Netplay room data is short-lived, with no persistent record on RomM beyond the [Netplay Cleanup scheduled task](../administration/scheduled-tasks.md) sweep. Passwords protect room access but aren't stored long-term.

## Troubleshooting

- **"Failed to start game"**: Netplay server-side config is broken. Operator: check `docker logs romm | grep -i netplay`. Usually a misconfigured ICE server URL.
- **Other players can't see my room**: either they're not on your RomM (shouldn't happen if they have accounts) or the WebSocket connection is broken. See [WebSocket Troubleshooting](../troubleshooting/authentication.md#400-bad-request-on-the-websocket-endpoint).
- **Game plays fine locally but Netplay glitches**: network round-trip is too high. Test with Players on the same LAN first; add TURN and re-test from outside.
- **Audio desync**: known WebRTC issue; try a different browser (Chrome is most-tested), or restart the session.

More in [Netplay Troubleshooting](../troubleshooting/netplay.md).
