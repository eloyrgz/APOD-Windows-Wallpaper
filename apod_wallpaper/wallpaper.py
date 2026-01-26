import logging
from pathlib import Path
from typing import Optional
from PIL import Image
import io
import os

log = logging.getLogger(__name__)

try:
    import win32api, win32con, win32gui
except Exception:
    win32api = win32con = win32gui = None


TILE_WALLPAPER = "0"
styles = {1: "0", 2: "2", 3: "6", 4: "10"}
style_names = {1: "center", 2: "stretch", 3: "fit", 4: "fill"}


def human_readable_size(number_bytes: float) -> str:
    for x in ['bytes', 'KB', 'MB']:
        if number_bytes < 1024.0:
            return "%3.2f%s" % (number_bytes, x)
        number_bytes /= 1024.0


def download_image(url: str, download_path: Path, proxies: Optional[dict] = None) -> Path:
    download_path = Path(download_path)
    download_path.mkdir(parents=True, exist_ok=True)
    filename = Path(os.path.splitext(os.path.basename(url))[0] + '.bmp')
    target = download_path / filename
    if target.exists():
        log.info("Image already downloaded: %s", target)
        return target
    log.info("Downloading image %s", url)
    from .api_client import dispatch_http_get
    r = dispatch_http_get(url, proxies=proxies)
    if r is None:
        raise RuntimeError("Failed to download image")
    file_size = human_readable_size(float(r.headers.get("content-length", 0)))
    log.info("Writing %s to disk...", file_size)
    Image.open(io.BytesIO(r.content)).save(str(target), 'BMP')
    log.info("Saved file %s", target)
    return target


def set_windows_wallpaper(file_path: Path, wallpaper_style: int) -> bool:
    try:
        style_val = styles[int(wallpaper_style)]
    except Exception:
        style_val = styles.get(4, "10")

    # Prefer pywin32 if available
    if win32api is not None:
        try:
            log.info("Setting wallpaper style %s", style_names.get(int(wallpaper_style), wallpaper_style))
            key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
            win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, style_val)
            win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, TILE_WALLPAPER)
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, str(file_path), 1 + 2)
            log.info("Wallpaper set (pywin32)")
            return True
        except Exception:
            log.exception("pywin32 method failed, attempting fallback")

    # Fallback: use stdlib winreg + ctypes to call SystemParametersInfoW
    try:
        import winreg
        import ctypes

        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02

        log.info("Setting wallpaper style %s (fallback)", style_names.get(int(wallpaper_style), wallpaper_style))
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, style_val)
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, TILE_WALLPAPER)
        winreg.CloseKey(key)

        # SystemParametersInfoW expects a unicode string path
        res = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(file_path), SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        if not res:
            raise OSError("SystemParametersInfoW failed")
        log.info("Wallpaper set (winreg/ctypes fallback)")
        return True
    except Exception:
        log.exception("Failed to set wallpaper using fallback methods")
        return False


# CNTLM / service management removed as legacy functionality
