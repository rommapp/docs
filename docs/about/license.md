---
title: License
description: How RomM is licensed, and what that means for you.
---

# License

## Core app: AGPLv3

The main [RomM application](https://github.com/rommapp/romm) is licensed under the [GNU Affero General Public License v3.0](https://choosealicense.com/licenses/AGPLv3/). In short, AGPLv3 says:

- **You can** use RomM privately, commercially, or at any scale.
- **You can** modify the source code however you want.
- **You must** make your modifications available under AGPLv3 if you distribute them _or_ run them as a network-accessible service for others.
- **You must** preserve copyright and license notices.

If you host a modified RomM and other people use it over the network, you owe them the source. This prevents the "hosted SaaS fork without upstream contributions" failure mode that's common with plain GPL. For most self-hosters this has zero practical effect, since you're running an unmodified version for yourself and the license doesn't constrain you. For companies thinking about shipping a modified RomM commercially, understand the AGPL obligations first.

Full license text: [rommapp/romm/blob/master/LICENSE](https://github.com/rommapp/romm/blob/master/LICENSE).

## Companion apps: varies

The RomM umbrella hosts several projects under different licenses:

| Project                                                               | License |
| --------------------------------------------------------------------- | ------- |
| [rommapp/romm](https://github.com/rommapp/romm)                       | AGPLv3  |
| [rommapp/argosy-launcher](https://github.com/rommapp/argosy-launcher) | AGPLv3  |
| [rommapp/grout](https://github.com/rommapp/grout)                     | MIT     |
| [rommapp/playnite-plugin](https://github.com/rommapp/playnite-plugin) | AGPLv3  |
| [rommapp/docs](https://github.com/rommapp/docs) (what you're reading) | CC0     |

Companion repos use more permissive licenses AGPLv3 or MIT because they're smaller, more-replaceable, and don't host the library. The AGPL network-service clause doesn't offer the same protection benefits there.

## Third-party components

Several third-party components ship with their own licenses: [EmulatorJS](https://emulatorjs.org/), [Ruffle](https://ruffle.rs/), Vue, FastAPI, and a long list of smaller dependencies. Their licenses apply to their respective code, and none of them override AGPLv3 on the RomM code itself. View the full list via `uv tree` in the backend and `npm ls` in the frontend. Redistribution respects each upstream's terms.

## FAQ

### Can I use RomM at work/for my company's gaming night?

Yes. AGPL doesn't restrict private or commercial use.

### Can I fork RomM and relicense my fork?

No. AGPL is a strong copyleft, so forks remain AGPL, and while you can add your own changes under AGPL you can't relicense the original code.

### Can I charge money for RomM-as-a-service?

Yes, but you owe your users the source, so you can't run a modified closed-source hosted RomM for paying customers.

### Can I sell ROMs through RomM?

No, as the sale of ROMs is not permitted in most jurisdictions.

### Is there a commercial/dual-license option?

Please reach out to us if you're interested in commercial licensing. We may be open to dual-licensing arrangements for certain use cases!

## See also

- [Credits](credits.md)
- [AGPLv3 overview](https://choosealicense.com/licenses/agpl-3.0/)
- Full license text: [LICENSE](https://github.com/rommapp/romm/blob/master/LICENSE)
