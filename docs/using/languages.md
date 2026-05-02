---
title: Languages
description: UI translation
---

# Languages

Pick the language you want for the UI, with the choice stored server-side so it follows you across devices. If you're not signed in (Kiosk mode), the UI picks based on browser `Accept-Language` and falls back to `en_US`.

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

## What gets translated

- All UI strings: menus, buttons, labels, tooltips, dialogs
- Error messages and notifications
- Help text and inline instructions

Not translated:

- **Game metadata**: titles, descriptions, genres come from metadata providers. English is usually the source language. IGDB has some localisation but coverage is uneven.
- **Your own content**: collection names, notes, user-uploaded media

## Contributing a translation

### Add missing strings to an existing locale

1. Fork [rommapp/romm](https://github.com/rommapp/romm).
2. Under `frontend/src/locales/<your-locale>/`, open the JSON/YAML files.
3. Add the missing keys (they're all present in `en_US` for reference).
4. Open a PR.

### Add a new locale

1. Create `frontend/src/locales/<your-locale>/` by copying the structure from `en_US`.
2. Translate.
3. Register the locale in the `frontend/src/locales/index.ts` file (the filename may change, so follow the pattern in the repo).
4. Open a PR.

See [Translations (i18n)](../developers/i18n.md) for the full contributor walkthrough.
