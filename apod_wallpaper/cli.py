import argparse
import logging
import shutil
from pathlib import Path
from .config import Config
from .api_client import get_apod_json
from .wallpaper import download_image, set_windows_wallpaper, style_names

log = logging.getLogger(__name__)


def print_banner() -> None:
    print(
        "\n\n"
        "\t`...     `..      `.         `.. ..        `.                  `.       `.......      `....     `.....    \n"
        "\t`. `..   `..     `. ..     `..    `..     `. ..               `. ..     `..    `..  `..    `..  `..   `.. \n"
        "\t`.. `..  `..    `.  `..     `..          `.  `..             `.  `..    `..    `..`..        `..`..    `..\n"
        "\t`..  `.. `..   `..   `..      `..       `..   `..           `..   `..   `.......  `..        `..`..    `..\n"
        "\t`..   `. `..  `...... `..        `..   `...... `..         `...... `..  `..       `..        `..`..    `..\n"
        "\t`..    `. .. `..       `.. `..    `.. `..       `..       `..       `.. `..         `..     `.. `..   `.. \n"
        "\t`..      `..`..         `..  `.. ..  `..         `..     `..         `..`..           `....     `.....    \n\n"
    )


def main(config_path: Path, once: bool = False) -> None:
    cfg = Config.from_file(config_path)

    content = get_apod_json(cfg.apod_url, cfg.api_key, proxies=cfg.proxies)
    if content is None:
        print("NASA APOD unavailable!")
        input()
        return

    if content.get('media_type') != 'image':
        print(f"Today's picture is a {content.get('media_type')}, please visit http://apod.nasa.gov/apod/astropix.html")
        input()
        return

    print_banner()
    print(content.get('title', '') + '\n')
    print(content.get('explanation', '') + '\n')
    url_img = content.get('hdurl', content.get('url'))
    filename = download_image(url_img, cfg.download_path, proxies=cfg.proxies)

    # If --once, set wallpaper with default style and exit
    if once:
        set_windows_wallpaper(filename, cfg.def_wallpaper_style)
    else:
        # Interactive style selection loop
        print("Select wallpaper style by entering its number and press Enter:")
        for k, v in style_names.items():
            print(f"  {k}: {v}")
        print("Enter any other key to exit.")

        user_input = cfg.def_wallpaper_style
        # apply the initial/default style first
        try:
            set_windows_wallpaper(filename, int(user_input))
        except Exception:
            pass

        while True:
            user_input = input("Style number (1-4) or other to exit: ").strip()
            if user_input.isnumeric() and 1 <= int(user_input) <= len(style_names):
                set_windows_wallpaper(filename, int(user_input))
            else:
                break

    # legacy cntlm handling removed


def cli_entry(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Set NASA APOD as Windows wallpaper")
    parser.add_argument("--config", "-c", default=str(Path.cwd() / "apod_wallpaper.conf"), help="Path to config file")
    parser.add_argument("--once", action="store_true", help="Download and set wallpaper once, then exit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable INFO logging")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO if args.verbose else logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')
    cfg_path = Path(args.config)
    try:
        main(cfg_path, once=args.once)
        return 0
    except Exception as e:
        log.exception("Error running CLI: %s", e)
        return 2


def cli_main() -> None:
    """Console entry point wrapper for setuptools/pyproject scripts."""
    raise SystemExit(cli_entry())

