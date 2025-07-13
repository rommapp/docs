## Scheduled tasks

Scheduled tasks can be enabled and configured with the following environment variables:

| Variable                                   | Description                                                  |     Value     |
| ------------------------------------------ | ------------------------------------------------------------ | :-----------: |
| ENABLE_SCHEDULED_RESCAN                    | Enable scheduled re-scanning of library                      |    `true`     |
| SCHEDULED_RESCAN_CRON                      | Cron expression for scheduled re-scanning                    | `"0 3 * * *"` |
| ENABLE_SCHEDULED_UPDATE_SWITCH_TITLEDB     | Enable scheduled updating of Switch TitleDB index            |    `true`     |
| SCHEDULED_UPDATE_SWITCH_TITLEDB_CRON       | Cron expression for scheduled updating of Switch TitleDB     | `"0 4 * * *"` |
| ENABLE_SCHEDULED_UPDATE_LAUNCHBOX_METADATA | Enable scheduled updating of LaunchBox metadata              |    `true`     |
| SCHEDULED_UPDATE_LAUNCHBOX_METADATA_CRON.  | Cron expression for scheduled updating of LaunchBox metadata | `"0 5 * * *"` |

### Scheduled re-scan

Users can opt to enable scheduled re-scans, and set the interval using Cron notation. Not that the scan will **not completely re-scan** every file, only catching those which have been added/updated.

### Switch titleDB update

Support was added for Nintendo Switch ROMs with filenames using the [titleid/programid format](https://wiki.gbatemp.net/wiki/List_of_Switch_homebrew_titleID) (e.g. 0100000000010000.xci). If a file under the `switch` folder matches the regex, the scanner will use the index to attempt to match it to a game. If a match is found, the IGDB handler will use the matched name as the search term.

The associated task updates the `/fixtures/switch_titledb.json` file at a regular interval to support new game releases.

### LaunchBox metadata update

RomM can also update the LaunchBox metadata database at a regular interval. This is onyl useful if you've enabled the LaunchBox metadata provider. The database is updated by downloading the latest version from the [LaunchBox Games Database](https://gamesdb.launchbox-app.com/) and replacing the existing one.

## File system watcher

RomM can also monitor the filesystem for events (files created/moved/deleted) and schedules a re-scan of the platform (or entire library is a new platform was added).

The watcher can be enabled and configured with the following environment variables:

| Variable                           | Description                                                         | Value  |
| ---------------------------------- | ------------------------------------------------------------------- | :----: |
| ENABLE_RESCAN_ON_FILESYSTEM_CHANGE | Enable re-scanning of library when filesystem changes               | `true` |
| RESCAN_ON_FILESYSTEM_CHANGE_DELAY  | Delay in minutes before re-scanning library when filesystem changes |  `5`   |

The watcher will monitor the `/library/roms` folder for changes to the filesystem, such as files being added, moved or deleted. It will ignore certain events (like modifying the file content or metadata), and will skip default OS files (like `.DS_Store` on mac).

When a change is detected, a scan will be scheduled for sometime in the future (default 5 minutes). If other events are triggered between now and the time at which the scan starts, more platforms will be added to the scan list (or the scan may switch to a full scan). This is done to reduce the number of tasks scheduled when many big changes happen to the library (mass upload, new mount, etc.)
