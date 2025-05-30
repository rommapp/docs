<div align="center">
    <img src="../../resources/romm/integrations/muos.svg" height="200px" width="200px" alt="romm[muos] isotipo">
</div>

<a href="https://muos.dev" target="_blank">muOS</a> is a Custom Firmware (CFW) primarily for handheld devices. Configurable, themeable, friendly, easy-to-use.

The <a href="https://github.com/rommapp/muos-app" target="_blank">muOS app</a> connects to your RomM instance and allows you to fetch games wirelessly from your Anbernic device.

## Setup

### muOS

We leverage the muOS [Archive Manager](https://muos.dev/help/archive) to install/update the app.

1. Head to the [latest release](https://github.com/rommapp/muos-app/releases/latest) and download the `romm_muOS_install_x.x.x.zip` file.
2. Move the **compressed** ZIP file to `/mnt/mmc/ARCHIVE` on your device.
3. Launch the manager from `Applications > Archive Manager` and select `romm_muOS_install_x.x.x.zip`.
4. Once installed, make a copy of `/mnt/mmc/MUOS/application/RomM/env.template`, rename it to `/mnt/mmc/MUOS/application/RomM/.env`, edit it (any method is fine, we recommend SSH) and set `HOST`, `USERNAME` and `PASSWORD`.
5. Launch the app from `Applications > RomM` and start browsing your collection.

### EmulationStation

We use PortMaster to install the app on devices running EmulationStation.

1. Download the `RomM App.sh` file and `RomM/` folder to the `roms/ports` on your device.
2. Make the `RomM App.sh` file executable by running `chmod +x RomM App.sh`.
3. Launch EmulationStation and navigate to the `Ports` section.
