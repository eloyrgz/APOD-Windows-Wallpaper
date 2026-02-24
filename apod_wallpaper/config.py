from pathlib import Path
import configparser
import logging

log = logging.getLogger(__name__)


class Config:
    def __init__(self, api_key: str, apod_url: str, download_path: Path, def_wallpaper_style: str, proxy_addr: str = None, proxy_port: str = None):
        self.api_key = api_key
        self.apod_url = apod_url
        self.download_path = Path(download_path).expanduser()
        self.def_wallpaper_style = def_wallpaper_style
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port

    @property
    def proxies(self):
        if self.proxy_addr and self.proxy_port:
            addr = self.proxy_addr
            # allow users to include a scheme in the address (http:// or https://)
            if addr.startswith("http://") or addr.startswith("https://"):
                base = addr
            else:
                # most corporate proxies speak plain HTTP for both http and https tunnelling
                base = f"http://{addr}"
            return {"http": f"{base}:{self.proxy_port}", "https": f"{base}:{self.proxy_port}"}
        return None

    @classmethod
    def from_file(cls, path: Path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        cp = configparser.ConfigParser(allow_no_value=True)
        cp.read(path)
        try:
            api_key = cp.get("api", "key")
            apod_url = cp.get("api", "url")
            proxy_addr = cp.get("proxy", "address") if cp.has_section("proxy") else None
            proxy_port = cp.get("proxy", "port") if cp.has_section("proxy") else None
            download_path = cp.get("default", "download_path")
            def_wallpaper_style = cp.get("default", "wallpaper_style")
        except Exception as e:
            log.error("Error reading config: %s", e)
            raise
        return cls(api_key=api_key, apod_url=apod_url, download_path=download_path, def_wallpaper_style=def_wallpaper_style, proxy_addr=proxy_addr, proxy_port=proxy_port)
