<!-- trunk-ignore-all(markdownlint/MD033) -->
<!-- trunk-ignore-all(markdownlint/MD041) -->

RomM requires one of these folder structures for proper operation. It will first attempt to detect **Structure A (recommended)**, and if not found, will fall back to **Structure B**. This auto-detection ensures flexibility while encouraging organization best practices.

## Folder Organization

RomM organizes content in two main categories: ROMs and BIOS files.

- **Structure A (Recommended)**: Both ROMs and BIOS files have their own dedicated root folders, with platform folders inside each.

    - `/roms/{platform}/` - Contains all game files for that platform
    - `/bios/{platform}/` - Contains all BIOS files for that platform

- **Structure B (Fallback)**: Each platform has its own root folder containing both a ROMs folder and a BIOS folder.
    - `/{platform}/roms/` - Contains all game files for that platform
    - `/{platform}/bios/` - Contains all BIOS files for that platform

<!-- prettier-ignore -->
!!! note
    The BIOS folder is entirely optional and only needed for platforms that require BIOS files.

When using Docker, the volume mount point differs based on your chosen structure:

- **Structure A**: Mount the parent folder of the `roms` folder
- **Structure B**: Mount the parent folder of the `platform` folders

For multifile games (games stored as folders with multiple files or folders inside), RomM will detect special folders inside the game and will display with special tags in the webUI:

- `dlc`
- `hack`
- `manual`
- `mod`
- `patch`
- `update`
- `demo`
- `translation`
- `prototype`

<!-- prettier-ignore -->
!!! tip
  For folder naming conventions, review the [Platform Support](../Platforms-and-Players/Supported-Platforms.md) section. To override default system names in the folder structure (if your directories are named differently), see the [Configuration File](Configuration-File.md) section.

<table>
 <tr>
    <th style="text-align: center"><b>Structure A (recommended)</b></tthd>
    <th style="text-align: center"><b>Structure B (fallback)</b></th>
 </tr>
 <tr>
  <td style="text-align: center">
    <code>library/roms/{platform}/{game}</code>
  </td>
  <td style="text-align: center">
    <code>library/{platform}/roms/{game}</code>
  </td>
 </tr>
 <tr>
    <td>
      <pre style="font-size: 0.85em;">
        library/
        ├─ roms/
        │  ├─ gbc/
        │  │  ├─ game_1.gbc
        │  │  └─ game_2.gbc
        │  │
        │  ├─ gba/
        │  │  ├─ game_3.gba
        │  │  └─ game_4/
        │  │     ├─ game_4.gba
        │  │     ├─ dlc
        │  │     │  ├─ game_4_dlc_1.7z
        │  │     │  └─ game_4_dlc_2.7z
        │  │     ├─ hack
        │  │     │  └─ game_4_hardmode.rar
        │  │     ├─ manual
        │  │     │  └─ game_4_manual.pdf
        │  │     ├─ mod
        │  │     │  └─ game_4_crazy_mode.zip
        │  │     ├─ patch
        │  │     │  └─ game_4_patch_v1.1.zip
        │  │     ├─ update
        │  │     ├─ demo
        │  │     ├─ translation
        │  │     └─ prototype
        │  │
        │  └─ ps/
        │     ├─ game_5/
        │     │   ├─ game_5_cd_1.iso
        │     │   └─ game_5_cd_2.iso
        │     │
        │     └─ game_6.iso
        │
        └─ bios/
           ├─ gba/
           │  └─ gba_bios.bin
           │
           └─ ps/
              ├─ scph1001.bin
              ├─ scph5501.bin
              └─ scph5502.bin
      </pre>
    </td>
    <td>
      <pre style="font-size: 0.85em;">
        library/
        ├─ gbc/
        │  └─ roms/
        │     ├─ game_1.gbc
        │     └─ game_2.gbc
        │
        ├─ gba/
        │  ├─ roms/
        │  │  ├─ game_3.gba
        │  │  └─ game_4/
        │  │     ├─ game_4.gba
        │  │     ├─ dlc
        │  │     │  ├─ game_4_dlc_1.7z
        │  │     │  └─ game_4_dlc_2.7z
        │  │     ├─ hacks
        │  │     │  └─ game_4_hardmode.rar
        │  │     ├─ manuals
        │  │     │  └─ game_4_manual.pdf
        │  │     ├─ mods
        │  │     │  └─ game_4_crazy_mode.zip
        │  │     ├─ patch
        │  │     │  └─ game_4_patch_v1.1.zip
        │  │     ├─ update
        │  │     ├─ demo
        │  │     ├─ translation
        │  │     └─ prototype
        │  │
        │  └─ bios/
        │     └─ gba_bios.bin
        │
        └─ ps/
           ├─ roms/
           │  ├─ game_5/
           │  │  ├─ game_5_cd1.iso
           │  │  └─ game_5_cd2.iso
           │  │
           │  └─ game_6.iso
           │
           └─ bios/
              ├─ scph1001.bin
              ├─ scph5501.bin
              └─ scph5502.bin
      </pre>
    </td>
 </tr>
</table>

<!-- prettier-ignore -->
!!! note
  RomM can be setup without a prior folder structure. If files are manually uploaded from the webUI, RomM will automatically create the folder **Structure A**

## Configuration file

RomM's behavior can be customized using a `config.yml` file or through the `Library Management` page in the `Settings` menu. You can grab the example <a href="https://github.com/rommapp/romm/blob/master/examples/config.example.yml" target="_blank" rel="noopener noreferrer">config.example.yml</a> file and adapt it to your library.

What is shown in the `Library Management` page is the content of the `config.yml`. For more details read the [configuration file](Configuration-File.md) section.

## Naming Convention

### Tag Support

Games can be tagged with region, revision, or other tags by using parentheses in the file name. Additionally, you can set the region and language by adding a prefix: `(USA)`, `[reg-J]`, `(French)`, `[De]`.

- Revision tags must be prefixed with `rev` or `rev-` (e.g. `rev v1` or `rev-1`)
- Other tags will also be imported, for example: `tetris [1.0001](HACK)[!].gba`

Tags can be used to search for games in the search bar. For example, searching for `(USA)` will return all games with the USA tag.
