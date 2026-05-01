---
title: Netplay Troubleshooting
description: Fix EmulatorJS Netplay issues
---

# Netplay Troubleshooting

Netplay uses WebRTC + ICE servers for peer-to-peer connections, so most issues are ICE-related.

## `Failed to start game`

The most common error, and almost always the operator-side config:

1. **Is Netplay enabled?** `emulatorjs.netplay.enabled: true` in `config.yml`.
2. **Are ICE servers configured?** The operator needs at least one STUN server in `emulatorjs.netplay.ice_servers`. Without any, NAT traversal can't begin.
3. **ICE server URLs reachable?** RomM can't talk to `stun.l.google.com:19302` if your server has no outbound internet. Sounds silly but happens in air-gapped labs.

Full config: [Configuration File → `emulatorjs.netplay`](../reference/configuration-file.md#emulatorjsnetplay-new-in-50).

## Can't see the room

You created a room as host but other players don't see it.

- **They need accounts on your instance.** Netplay doesn't federate, which means a user with no account or on a different instance can't see or join.
- **WebSocket connection is broken.** Open devtools → Network → WS tab. If socket.io is disconnecting, see [Authentication Troubleshooting → WebSockets](authentication.md#400-bad-request-on-the-websocket-endpoint).
- **Other player didn't open the Netplay panel.** They need to click the 🌐 icon on the emulator toolbar to see the room list.

## Joined but video never appears

- **Host's browser stopped streaming.** Check host's tab is still foregrounded, because browsers throttle background tabs.
- **NAT traversal failed.** STUN couldn't hole-punch, and you have no TURN configured. Add a TURN server (see [Netplay → ICE servers](../using/netplay.md#ice-servers-the-nat-stuff)).
- **Symmetric NAT on one end.** Corporate networks and some carrier-grade NAT can't be STUN-traversed, only TURN (relay) will work.

## High lag / input delay

Normal Netplay delay is 50–150 ms, for any number higher:

- **You're routing through TURN.** TURN relays add latency proportional to your distance from the TURN server. Pick a TURN server geographically close to both players, or set up your own [coturn](https://github.com/coturn/coturn).
- **Host has slow uplink.** The host is streaming video to everyone, so if upload bandwidth is tight, lag spikes.
- **Weak host CPU.** The host runs the emulator AND encodes the video stream, so a weak CPU can cause lag.

## Desync

Different players' screens diverge over time (you do a move but they don't see it):

- **Browser tab backgrounded.** Browsers throttle, keep both tabs foregrounded.
- **Core-specific bug.** Not all cores handle Netplay cleanly!

## Audio crackle / cuts out on the client side

WebRTC audio is known to be fragile:

- **Use Chrome.** Its WebRTC implementation is the most mature.
- **Restart the session**. Audio sometimes recovers only after a full room teardown.

## Room disappears after the host leaves

When the host disconnects, the room is cleaned up (either immediately or by the next [Netplay Cleanup scheduled task](../administration/scheduled-tasks.md) sweep). If you want your session back, the host can recreate the room and have other players rejoin.

## Still stuck?

- Browser devtools Console: client-side log
- `chrome://webrtc-internals`: live ICE / WebRTC stats on Chrome
- [Discord](https://discord.gg/romm) `#romm-support` with both sides' error text

## See also

- [Using → Netplay](../using/netplay.md): how Netplay works and how to configure it
