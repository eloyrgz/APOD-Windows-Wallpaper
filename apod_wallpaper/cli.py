import argparse
import logging
import shutil
import os
from pathlib import Path
from .config import Config
from .api_client import get_apod_json, dispatch_http_get
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

    def show_and_apply(item):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception:
            pass
        print_banner()
        print(item.get('title', '') + '\n')
        print(item.get('explanation', '') + '\n')
        url_img_local = item.get('hdurl', item.get('url'))
        fname = download_image(url_img_local, cfg.download_path, proxies=cfg.proxies)
        try:
            set_windows_wallpaper(fname, int(cfg.def_wallpaper_style))
        except Exception:
            pass
        # Reprint the style selection and waiting prompt to match initial display
        print("Select wallpaper style by entering its number:")
        for k, v in style_names.items():
            print(f"  {k}: {v}")
        print("Press 1-4 repeatedly to change style; press any other key to exit.")
        print("Waiting for keypress... (1-4 change style, n download new image, other to exit)")
        return fname

    # If --once, set wallpaper with default style and exit
    if once:
        set_windows_wallpaper(filename, cfg.def_wallpaper_style)
    else:
        # Interactive style selection loop
        print("Select wallpaper style by entering its number:")
        for k, v in style_names.items():
            print(f"  {k}: {v}")
        print("Press 1-4 repeatedly to change style; press any other key to exit.")

        user_input = cfg.def_wallpaper_style
        # apply the initial/default style first
        try:
            set_windows_wallpaper(filename, int(user_input))
        except Exception:
            pass

        # Prefer single-key input on Windows (no Enter required)
        try:
            import msvcrt

            print("Waiting for keypress... (1-4 change style, n download new image, other to exit)")
            while True:
                ch = msvcrt.getwch()
                if ch in ('1', '2', '3', '4'):
                    set_windows_wallpaper(filename, int(ch))
                elif ch in ('n', 'N'):
                    # fetch a random APOD (count=1)
                    url = f"{cfg.apod_url}count=1&api_key={cfg.api_key}"
                    r = dispatch_http_get(url, proxies=cfg.proxies)
                    if r is None:
                        print("Failed to fetch new image")
                        continue
                    try:
                        data = r.json()
                    except Exception:
                        print("Invalid response for new image")
                        continue
                    # API returns a list when using count
                    if isinstance(data, list) and data:
                        item = data[0]
                    elif isinstance(data, dict):
                        item = data
                    else:
                        print("No image returned")
                        continue
                    if item.get('media_type') != 'image':
                        print("Fetched item is not an image")
                        continue
                    # show details, download and apply (same as initial display)
                    filename = show_and_apply(item)
                else:
                    break
        except Exception:
            # Fallback for non-Windows or if msvcrt unavailable: line-based input
            while True:
                user_input = input("Style number (1-4), n for new image, or other to exit: ").strip()
                if user_input.lower() == 'n':
                    url = f"{cfg.apod_url}count=1&api_key={cfg.api_key}"
                    r = dispatch_http_get(url, proxies=cfg.proxies)
                    if r is None:
                        print("Failed to fetch new image")
                        continue
                    try:
                        data = r.json()
                    except Exception:
                        print("Invalid response for new image")
                        continue
                    if isinstance(data, list) and data:
                        item = data[0]
                    elif isinstance(data, dict):
                        item = data
                    else:
                        print("No image returned")
                        continue
                    if item.get('media_type') != 'image':
                        print("Fetched item is not an image")
                        continue
                    filename = show_and_apply(item)
                elif user_input.isnumeric() and 1 <= int(user_input) <= len(style_names):
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

