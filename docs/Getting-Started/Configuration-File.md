Below is a breakdown of each section of the `config.yml` file and its purpose:

### `exclude`

This section lets you tell RomM which platforms, ROMs, or files to ignore during scanning.

- **platforms**
  Exclude entire platforms (folders) from being scanned.
  Example:

    ```yaml
    platforms: ["ps", "ngc", "gba"]
    ```

- **roms**
  Fine-tune which ROMs or files are excluded.

    - **single_file**
      Applies to ROMs that are single files (not in subfolders).

        - **extensions**: Exclude files by extension.
          Example:
            ```yaml
            extensions: ["xml", "txt"]
            ```
        - **names**: Exclude files by name or pattern (supports Unix wildcards).
          Example:
            ```yaml
            names: ["info.txt", "._*", "*.nfo"]
            ```

    - **multi_file**
      Applies to ROMs stored as folders (multi-disc, with DLC, etc.).
        - **names**: Exclude entire folders by name.
          Example:
            ```yaml
            names: ["final fantasy VII", "DLC"]
            ```
        - **parts**: Exclude specific files inside multi-file ROM folders.
            - **names**: Exclude files by name or pattern.
              Example:
                ```yaml
                names: ["data.xml", "._*"]
                ```
            - **extensions**: Exclude files by extension.
              Example:
                ```yaml
                extensions: ["xml", "txt"]
                ```

---

### `system`

Customize how RomM interprets your folder and platform names.

- **platforms**
  Map your custom folder names to RomM's recognized platform names.
  Example:

    ```yaml
    platforms: { gc: "ngc", psx: "ps" }
    ```

    This treats a `gc` folder as GameCube (`ngc`) and `psx` as PlayStation (`ps`).

- **versions**
  Associate a platform with its main version. This also tells RomM to fetch medatata from the main version source.
  Example:
    ```yaml
    versions: { naomi: "arcade" }
    ```

---

### `filesystem`

Specify the folder name where your ROMs are located if it differs from the default. For example, if your `roms` folder it's named `my_roms` (`/home/user/library/my_roms`), set this accordingly.

Example:

```yaml
filesystem: { roms_folder: "my_roms" }
```

---

!!! tip
You can find examples of full binded <a href="https://github.com/rommapp/romm/blob/release/examples/config.batocera-retrobat.yml" target="_blank" rel="noopener noreferrer">batocera</a> or <a href="https://github.com/rommapp/romm/blob/release/examples/config.es-de.example.yml" target="_blank" rel="noopener noreferrer">es-de</a> config files.

!!! warning
Only uncomment or add the lines you need. Any omitted or empty sections will use RomM's defaults.
For a full example, see the <a href="https://github.com/rommapp/romm/blob/release/examples/config.example.yml" target="_blank" rel="noopener noreferrer">config.example.yml</a> file.
