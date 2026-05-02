---
title: Netplay
description: Play games with friends in real time
---

# Netplay

**Netplay** lets you play [in-browser](in-browser-play/emulatorjs.md) with other users in real time: co-op, turn-based, or party games, shared across the internet.

## Prerequisites

- EmulatorJS Netplay enabled in `config.yml` (operator-level)
- ICE servers configured (STUN + TURN). Without them, Netplay only works when all players are on the same LAN.
- All players need access to your instance, as Netplay doesn't proxy the ROM to people without accounts.

See [Configuration File → `emulatorjs.netplay`](../reference/configuration-file.md#emulatorjsnetplay) for the operator-side setup.

## Hosting and joining

The host creates a room with an optional password from a supported game and becomes Player 1. Up to three more players can join as Players 2-4 (core-dependent, some only support 2). Other players must be on the same instance, since Netplay doesn't federate across instances.

## Controls

Every player controls their own gamepad/keyboard locally, and inputs are sent to the host, which runs the game and broadcasts video. Slight lag is expected over the internet (~50–150 ms typical), with higher latency on transatlantic hops or when using TURN servers.

## ICE servers (the NAT stuff)

WebRTC, the protocol Netplay uses, needs help to punch through some consumer routers. That's what ICE (STUN + TURN) servers do:

- **STUN**: helps two peers find each other's public IPs, and usually works unless one of you is behind symmetric NAT.
- **TURN**: relays traffic when STUN can't, but is more resource-intensive, and most free TURN services have quotas.

## Limitations

- **Not all cores support Netplay!** SNES9x, Mupen64Plus, Mednafen PSX, Genesis Plus GX are the most battle-tested.
- **Frame-perfect fighting isn't realistic.** Netplay is for casual co-op, not tournament-level fighting games, use something like [FightCade](https://www.fightcade.com/) for that.
- **All players need an account.** There's no "join a friend's game without an account", guests need at least a Viewer account on your instance.
- **RTC over TURN uses real bandwidth.** Hosting a 4-player N64 session over TURN can saturate a modest uplink.

## Security

Netplay room data is short-lived, with no persistent record beyond the [Netplay Cleanup scheduled task](../administration/scheduled-tasks.md) sweep. Passwords protect room access but aren't stored long-term.

## Troubleshooting

- **Other players can't see my room**: either they're not on your instance (shouldn't happen if they have accounts) or the WebSocket connection is broken (see [WebSocket Troubleshooting](../troubleshooting/authentication.md#400-bad-request-on-the-websocket-endpoint)).
- **Game plays fine locally but Netplay glitches**: network round-trip is too high, test with players on the same LAN first, then add TURN and re-test from outside.
- **Audio desync**: Try a different browser (Chrome should work well), or restart the session.

More in [Netplay Troubleshooting](../troubleshooting/netplay.md).
