<!-- trunk-ignore-all(markdownlint/MD033) -->
<!-- trunk-ignore-all(markdownlint/MD041) -->

<div align="center">
    <img src="../../resources/romm/integrations/playnite.svg" height="200px" width="200px" alt="romm[playnite] isotipo">
</div>

<a href="https://playnite.link" target="_blank">Playnite</a> is an open source video game library manager with one simple goal: To provide a unified interface for all of your games.

<a href="https://github.com/rommapp/playnite-plugin" target="_blank">This plugin</a> allows you to import your RomM library into Playnite. It queries the RomM API to create Playnite library entires for each of your games. Installing a game in Playnite will download it from RomM and store it on your system, allowing you to launch it in your emulator of choice.

## Installation

- Option A: Open this link in your browser to launch Playnite and install the plugin automatically: `playnite://playnite/installaddon/RomM_9700aa21-447d-41b4-a989-acd38f407d9f`
- Option B: Download the plugin from the [Playnite add-ons website](https://playnite.link/addons.html#RomM_9700aa21-447d-41b4-a989-acd38f407d9f)
- Option C: In Playnite, go to `Menu` -> `Add-ons...` -> `Browse` -> `Libraries`, search for `RomM`, and click `Install`
- Option D: Download the latest release from the [releases page](https://github.com/rommapp/playnite-plugin/releases/latest) and install it manually by dragging the `.pext` file onto Playnite

## Setup

### Emulators

The plugin requires that you have **at least 1 emulator installed** on your system and configured in Playnite. You can use a built-in emulator or a custom one. **If no emulators are installed and configured, you won't be able to complete setup!** To set up an emulator, go to `Menu` -> `Library` -> `Configure Emulators...` -> `Add emulator...`.

### Settings

The plugin needs to be configured before it can be used. To do this, go to `Menu` -> `Library` -> `Configure Integrations...` -> `RomM`.

#### Authentication

You'll need to enter the host URL of your RomM instance, as well as a username and password. Passwords are stored in plaintext in Playnite, so it's recommended to use a separate account with the "VIEWER" role. **The host URL has the include the protocol (http/https) and should not include a trailing slash, e.g. `https://romm.example.com`.**

#### Emulator path mappings

| Field            | Description                                                | Example           | Required |
| ---------------- | ---------------------------------------------------------- | ----------------- | -------- |
| Emulator         | A built-in (or custom) emulator                            | Dolphin           | ✓        |
| Emulator Profile | A built-in (or custom) emulator profile                    | Nintendo GameCube | ✓        |
| Platform         | The platform or console                                    | Nintendo GameCube | ✓        |
| Destination Path | The path where downloaded ROMs will be stored              | `C:\roms\gc`      | ✓        |
| Auto-extract     | Whether compressed files should be extracted automatically |                   |          |
| Enabled          | Whether the mapping is enabled                             |                   |          |

## Importing your library

Once you've set up the plugin, you can import your library by going to `Menu` -> `Library` -> `Import RomM library`. All games matching the emulator path mappings will be imported into Playnite.

Installing a game will download it from RomM and store it in the destination path. You can then launch the game from Playnite, and it will be launched using the configured emulator.

By default, compressed files will be extracted automatically into a folder matching the game's name. You can modify this behavior in the settings page.
