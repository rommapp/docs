---
title: Languages
description: Switch the RomM UI language, 19 locales supported in 5.0.
---

# Languages

RomM's UI is translated into 19 locales. Pick yours from **Profile → User Interface → Language**. The change is immediate: no reload, no re-login.

## Supported locales

| Code    | Language                         |
| ------- | -------------------------------- |
| `en_US` | English (United States), default |
| `en_GB` | English (United Kingdom)         |
| `es_ES` | Spanish (Spain)                  |
| `fr_FR` | French                           |
| `de_DE` | German                           |
| `it_IT` | Italian                          |
| `pt_BR` | Portuguese (Brazil)              |
| `ja_JP` | Japanese                         |
| `ko_KR` | Korean                           |
| `ru_RU` | Russian                          |
| `pl_PL` | Polish                           |
| `cs_CZ` | Czech                            |
| `hu_HU` | Hungarian                        |
| `ro_RO` | Romanian                         |
| `bg_BG` | Bulgarian                        |
| `zh_CN` | Chinese (Simplified)             |
| `zh_TW` | Chinese (Traditional)            |

Two more ship as work-in-progress with partial coverage. Check the language dropdown to see the current list.

## What gets translated

- All UI strings: menus buttons, labels, tooltips, dialogs.
- Error messages and notifications.
- Help text and inline instructions.

Not translated:

- **Game metadata**: titles, descriptions, genres come from metadata providers. English is usually the source language. IGDB has some localisation but coverage is uneven.
- **Your own content**: collection names, notes, user-uploaded media.
- **Docs site** (what you're reading): English only in 5.0.

## Missing strings

If a translation is incomplete, you'll see the English fallback for untranslated strings. This is intentional: better than showing a broken UI in a half-translated locale.

Spotted something missing? Help translate it, see below.

## Contributing a translation

### Add missing strings to an existing locale

1. Fork [rommapp/romm](https://github.com/rommapp/romm).
2. Under `frontend/src/locales/<your-locale>/`, open the JSON / YAML files.
3. Add the missing keys. They're all present in `en_US` for reference.
4. Open a PR.

### Add a new locale

1. Create `frontend/src/locales/<your-locale>/` by copying the structure from `en_US`.
2. Translate.
3. Register the locale in the `frontend/src/locales/index.ts` file (the filename may change, so follow the pattern in the repo).
4. Open a PR.

Partial translations are welcome. We'd rather have a 70%-translated locale up for people to improve than hold out for 100%.

See [Translations (i18n)](../developers/i18n.md) for the full contributor walkthrough.

## Persistence

Your language choice is stored server-side on your user record, so it follows you across devices. If you're not signed in (Kiosk mode, for example), the UI picks based on browser `Accept-Language` header and falls back to `en_US`.

## Locale-specific notes

### Right-to-left (RTL)

No RTL locales in 5.0. Arabic and Hebrew translations may land in a future release, because the UI needs some layout work before it can present them cleanly.

### CJK typography

CJK locales (Japanese, Korean, Chinese simplified/traditional) use the browser's default system font stack. Some game titles with rare glyphs may render inconsistently across OSes. That's a browser font issue, not a RomM one.

## Docs i18n

The docs site is currently English-only. Localising docs is a much bigger commitment than localising the app. If you'd like to help, open an issue on [rommapp/docs](https://github.com/rommapp/docs) and we can discuss scope.

## Related

- [User Interface settings](account-and-profile.md): full list of personal UI preferences.
- [Console Mode](console-mode.md): same locale selection applies.
- [Developers → Translations (i18n)](../developers/i18n.md): contributor guide.
