---
title: Parental Controls
description: Age limits on permission groups and users
---

# Parental Controls

Parental controls hide games above an age from the members of a [permission group](users-and-roles.md#permission-groups), or from a single user. You set them in the group and user dialogs under Administration.

Two settings make up a rule:

- **Age limit**: members only see games rated for this age or younger, from `0` to `21`, with no limit as the default.
- **Hide unrated games**: also hides every game that no known rating covers, even with no age limit set. Without it, an unrated game stays visible whatever the limit, because there's nothing to judge it by.

## Who a rule applies to

- **Groups** carry a limit and a hide-unrated switch for every member. A user with no group follows the server's default group, its age settings included.
- **Users** can replace either setting of their group. A user's own value wins, and an unset value inherits the group's, so you can give one member a stricter or looser limit than the rest of the group.
- **Admins** are never limited, whatever their group says, because they bypass permission groups entirely.

## Where it applies

An age rule hides a game the same way as a [hidden ROM](users-and-roles.md#hidden-entities), so it stays out of everything a member can reach: the gallery, search, collections (smart and virtual ones included), server stats, recommendations, the Jukebox, feeds for [feed clients](../ecosystem/feed-clients.md), netplay rooms, device installs and sync, and every per-ROM route such as downloads, manuals and screenshots. A direct request for one answers as if the game didn't exist, usually with a `404`.

## How a game's age is worked out

Each game stores one minimum age, the **strictest** age any of its ratings sets, which is recomputed whenever that metadata changes. Ratings are read from:

| Source                        | What RomM reads                                                     |
| ----------------------------- | ------------------------------------------------------------------- |
| IGDB                          | Every age rating, from any board                                    |
| ScreenScraper                 | Every classification, from any board                                |
| LaunchBox                     | The ESRB rating                                                     |
| Steam                         | The required age, when the store sets one                           |
| Manual metadata (Edit dialog) | The game's own age rating list, which **replaces** all of the above |

As on the game page, the manual list overrides the providers entirely, so you can loosen a rating as well as tighten it. Manual entries take the form `BOARD:RATING`, such as `ESRB:T` or `PEGI:12`.

A game counts as unrated when it has no ratings at all, or only ones that can't be read (an unknown board, or an unrecognised value).

### Rating boards

Boards that rate with letters map to the youngest age each rating admits:

| Board           | Ratings                                                                   |
| --------------- | ------------------------------------------------------------------------- |
| ESRB            | `EC` 3, `E` 6, `KA` (Kids to Adults) 6, `E10` 10, `T` 13, `M` 17, `AO` 18 |
| CERO            | `A` 0, `B` 12, `C` 15, `D` 17, `Z` 18                                     |
| ACB (also OFLC) | `G` 0, `PG` 8, `M` 15, `MA15` 15, `R18` 18, `X18` 18, `RC` 18             |
| BBFC            | `U` 0, `PG` 8, `12` 12, `12A` 12, `15` 15, `18` 18, `R18` 18              |

Boards that rate with numbers use the number as the age, with `L` or `ALL` meaning any age: PEGI, USK, GRAC, ClassInd (also DJCTQ), ScreenScraper's own `SS` classification, ELSPA and JV.

ESRB's `E` maps to 6 rather than to "everyone" because it's treated as the pre-1998 Kids to Adults floor, so a 3-year limit hides `E` games but shows `EC` ones.

## Existing libraries

The upgrade to 5.4 computes the minimum age for every game already in the database, so limits work straight away. A game picks up new ratings on its next metadata refresh, and its age follows.

## API

The permission group schemas (`PermissionGroupSchema`, `PermissionGroupCreate` and `PermissionGroupUpdate`) and the user permission schemas (`UserPermissionsSchema` and `UserPermissionsUpdate`) carry two fields:

| Field               | On a group                          | On a user                                         |
| ------------------- | ----------------------------------- | ------------------------------------------------- |
| `age_limit`         | `0` to `21`, or `null` for no limit | `0` to `21`, or `null` to inherit the group's     |
| `hide_unrated_roms` | `true` or `false`                   | `true`, `false`, or `null` to inherit the group's |

The update payloads (`PUT /api/permissions/groups/{id}` and `PUT /api/permissions/users/{user_id}`) apply both fields only when `set_age_settings` is `true`, and then write them exactly as given, so an update that leaves `set_age_settings` out never touches its age rule. Both routes require `users.write` and an admin caller.
