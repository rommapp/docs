<!-- trunk-ignore-all(markdownlint/MD041) -->

## Prerequisites

Before getting started, install the [Community Apps plugin](https://forums.unraid.net/topic/38582-plug-in-community-applications/) for Unraid.

### Docker network

You'll want to create a custom bridge-type network for both containers to communicate with each other. This will prevent a number of common issues Unraid users tend to come across during setup. This can be done with the following command: `docker network create romm`, and you can verify it worked with `docker network ls`.

![console output](https://github.com/user-attachments/assets/bac31998-1911-4085-b115-8dd93d519b8b)

### MariaDB

MariaDB is required to run RomM, so install it from the plugin registry. Only the [official](https://hub.docker.com/_/mariadb) and [linuxserver](https://github.com/linuxserver/docker-mariadb/pkgs/container/mariadb) versions are supported, but **the official version is preferred**.

![community apps search results for MariaDB](https://github.com/user-attachments/assets/76f4b6ef-5b63-454f-9357-d2920b9afd0e)

Now fill in all the environment variables; descriptions of the options and sensible defaults are listed in the [example docker-compose.yml](https://github.com/rommapp/romm/blob/release/examples/docker-compose.example.yml) file.

<!-- prettier-ignore -->
!!! warning
    The network type must be set to `Custom: romm`

![MariaDB environment variables](https://github.com/user-attachments/assets/a11906c5-25b2-46f1-906b-451a9ee39dca)

## Installation

From the Unraid dashboard, click `APPS` in the navigation bar. In the search bar, search for `romm`, and install the app listed as "OFFICIAL". This one is maintained by our team and is the most up-to-date.

![RomM official app](https://github.com/user-attachments/assets/57c4d47a-8604-4e8d-b05a-84dd68dda124)

## Configuration

Configure the required environment variables, ports and paths as per the [example docker-compose.yml](https://github.com/rommapp/romm/blob/release/examples/docker-compose.example.yml) file.

<!-- prettier-ignore -->
!!! warning
    The network type must also be set to `Custom: romm`

![RomM docker tab](https://github.com/user-attachments/assets/4c4210c2-ed00-4790-a945-65cbe33620b0)

Apply the changes, then head to the `DOCKER` tab. You should see both containers in a running state, and can access RomM using the IP:PORT of the container (highlighted below).

![RomM and MariaDB running](https://github.com/user-attachments/assets/cba26de1-d2c9-4fff-88d8-bc7701f0dd88)

<!-- prettier-ignore -->
!!! warning
    It's strongly recommended to backup the `appdata` folder (or mount it in a safe location) before updating, since tearing down the container will wipe the resources (covers, screenshots, etc.)

## Video tutorial

[DemonWarriorTech](https://www.youtube.com/@DemonWarriorTech) has published [How to Install RomM on Unraid (Beginner Friendly)](https://www.youtube.com/watch?v=Oo5obHNy2iw) on installing and running RomM on Unraid for Beginners with an in depth instructions and explanation of the software install and how to use it.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Oo5obHNy2iw/0.jpg)](https://www.youtube.com/watch?v=Oo5obHNy2iw)

[AlienTech42](https://www.youtube.com/@AlienTech42) has published [a great video](https://www.youtube.com/watch?v=ls5YcsFdwLQ) on installing and running RomM on Unraid. While a bit out of date vis-a-vis install instructions, it's still very useful for general setup and debugging. Check it out!

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ls5YcsFdwLQ/0.jpg)](https://www.youtube.com/watch?v=ls5YcsFdwLQ)

## Unraid community support

You can find a [support thread](https://forums.unraid.net/topic/149738-support-eurotimmy-romm-rom-manager-by-zurdi15/) in the unraid forums.

## Shout-outs

We want to give a special shout-out to @Smurre95 and @sfumat0 for their help documenting this process, and working towards getting RomM listed in CA. 🤝
