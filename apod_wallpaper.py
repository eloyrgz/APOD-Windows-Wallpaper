#!/usr/bin/env python
# -*-coding:utf-8-*-
import sys
import requests
import logging
import os
from PIL import Image
import io
import configparser
import win32api, win32con, win32gui
import subprocess

TILE_WALLPAPER = "0" # 1 tiles image if style is center

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y/%d/%m %H:%M:%S', level=logging.ERROR)
log = logging.getLogger()

config = configparser.ConfigParser()
try:
    config.read(os.getcwd() + "/apod_wallpaper.conf")
    api_key = config.get("api", "key")
    apod_url = config.get("api", "url")
    px = config.get("proxy", "address") + ":" + config.get("proxy", "port")
    proxy = {"https": "https://" + px, "http": "http://" + px}
    path_local_proxy = config.get("proxy", "local_path")
    download_path = config.get("default", "download_path")
    def_wallpaper_style = config.get("default", "wallpaper_style")
except:
    log.error("Missing or wrong config file!")
    raise

styles = {1: "0", 2: "2", 3: "6", 4: "10"}
style_names = {1: "center", 2: "stretch", 3: "fit", 4: "fill"}


def dispatch_http_get(url, p=None):
    global proxy
    r = None
    try:
        log.info("Dispatching HTTP GET Request %s... ", url)
        r = requests.get(url, proxies=p)
        log.info("Retrieved response")
    except Exception as e:
        if proxy is not None and p is None:
            log.warning("Trying with proxy %s...", proxy)
            r = dispatch_http_get(url, proxy)
        else:
            log.error("HTTP GET Request Error: %s", e)
    return r


def human_readable_size(number_bytes):
    for x in ['bytes', 'KB', 'MB']:
        if number_bytes < 1024.0:
            return "%3.2f%s" % (number_bytes, x)
        number_bytes /= 1024.0


def download_image(url):
    filename = os.path.splitext(os.path.basename(url))[0]
    filename = os.path.join(download_path, filename + '.bmp')
    if os.path.isfile(filename):
        log.info("today's picture has been already downloaded before")
    else:
        log.info("Downloading image...")
        r = dispatch_http_get(url)
        file_size = human_readable_size(float(r.headers["content-length"]))
        log.info("writing %s to disk...", file_size)
        Image.open(io.BytesIO(r.content)).save(filename, 'BMP')
        log.info("saved file %s", filename)
    return filename


def set_windows_wallpaper(file_path, wallpaper_style):
    """
    Two registry values are set in the Control Panel\Desktop key. Based on
    which style is requested, numeric codes are set for the WallpaperStyle and
    TileWallpaper values:

    http://msdn.microsoft.com/en-us/library/bb773190(VS.85).aspx#desktop

    TileWallpaper
      0: The wallpaper picture should not be tiled
      1: The wallpaper picture should be tiled

    WallpaperStyle
      0:  The image is centered if TileWallpaper=0 or tiled if TileWallpaper=1
      2:  The image is stretched to fill the screen
      6:  The image is resized to fit the screen while maintaining the aspect
          ratio. (Windows 7 and later)
      10: The image is resized and cropped to fill the screen while maintaining
          the aspect ratio. (Windows 7 and later)
    """
    log.info("%s wallpaper", style_names[int(wallpaper_style)])
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, styles[int(wallpaper_style)])
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, TILE_WALLPAPER)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, file_path, 1 + 2)

def exit_program():
    log.info("Exit")
    sys.exit()

if __name__ == '__main__':
    if path_local_proxy is not None:
        if os.path.isfile(path_local_proxy):
            log.info("Opening cntlm at " + path_local_proxy)
            p=subprocess.Popen('\"'+path_local_proxy+'\"') 
            log.info("done")
        else:
            log.error("Local proxy file not found " + path_local_proxy)
            exit_program()
            
    log.info("Requesting content")
    content = dispatch_http_get(apod_url + "concept_tags=True&api_key=" + api_key)
    if content is None:
        print("NASA APOD unavailable!")
        input()
    else:
        content = content.json()
        if not content['media_type'] == "image":                
            print("\nToday's picture is a " + content['media_type'] + ", please visit http://apod.nasa.gov/apod/astropix.html")
            input()
        else:
            print(content['title'] + '\n')
            print(content['explanation'] + '\n')
            # Download image
            url_img = content['hdurl'] if 'hdurl' in content else content['url']
            filename = download_image(url_img)
            user_input = def_wallpaper_style
            while user_input.isnumeric() and int(user_input) <= len(styles):
                # Set wallpaper
                set_windows_wallpaper(filename, user_input)
                # wait for user input (1 to 4 change the wallpaper style, otherwise exit)
                user_input = input()
    if path_local_proxy is not None:
        log.info("closing cntlm")
        p.terminate()
    exit_program()
