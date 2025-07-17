<!-- trunk-ignore-all(markdownlint/MD033) -->
<!-- trunk-ignore-all(markdownlint/MD041) -->

While RomM supports every platform listed in the [Supported Platforms page](../Platforms-and-Players/Supported-Platforms.md), the list is not exhaustive, and you may have ROMs in your library for other platforms. To load those files into RomM, place them in a folder for each platform, and give it a name that's **all lowercase**, with **`-` to separate words**, and with **no white spaces**. For example, `pocket-challenge-v2` would map to `Pocket Challenge V2`, and display the default platform icon in the app.

Furthermore, only a portion of the supported platforms have custom icons built-in. If your library has platforms that aren't listed in [the platforms icons list](https://github.com/rommapp/romm/tree/release/frontend/assets/platforms), RomM will display a default fallback icon.

If you'd like to load your own custom icons for missing platforms, you can mount `/var/www/html/assets/platforms` to some local folder and place all of your custom **`.ico`** platform icons in there. You'll also want to download the ones [provided in this project](https://github.com/rommapp/romm/tree/release/frontend/assets/platforms) and place them in the same folder. If you'd like to use your own icons for platforms already supported by RomM, just replace the file with another using the exact same name.

**The name of the `.ico` file should match the slug of the platform on IGDB.** For example, the URL for the AmstradCPC is <https://www.igdb.com/platforms/acpc>, so the filename should be `acpc.ico`.

<img width="2459" alt="Screenshot 2023-09-15 at 10 45 04 AM" src="https://github.com/rommapp/romm/assets/3247106/1831c206-b431-41c2-9761-49c132f40ee0">
