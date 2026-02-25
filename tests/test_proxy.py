import os
import socket
from urllib.parse import urlparse

import pytest
import requests
from pathlib import Path

from apod_wallpaper.config import Config


def _proxies_from_env_or_config():
    env = os.environ.get("TEST_PROXY")
    if env:
        return {"http": env, "https": env}, env
    cfg_path = os.environ.get("APOD_CONFIG", "apod_wallpaper.conf")
    p = Path(cfg_path)
    if not p.exists():
        pytest.skip(f"Config file not found: {p}")
    cfg = Config.from_file(p)
    proxies = cfg.proxies
    if not proxies:
        pytest.skip("No proxy configured in config file")
    # Build a proxy URL for reachability checks
    proxy_url = None
    if cfg.proxy_addr and cfg.proxy_port:
        proxy_url = f"http://{cfg.proxy_addr}:{cfg.proxy_port}"
    return proxies, proxy_url


def _is_proxy_reachable(proxy_url: str, timeout: float = 3.0) -> bool:
    """Quick TCP connect to the proxy host:port to determine reachability."""
    try:
        p = urlparse(proxy_url)
        host = p.hostname or proxy_url
        port = p.port or (443 if p.scheme == "https" else 80)
        with socket.create_connection((host, port), timeout):
            return True
    except Exception:
        return False


def test_proxy_connects_to_apod():
    """Attempts a simple GET to the APOD endpoint using proxy from env or project config.

    Priority: `TEST_PROXY` env var. Fallback: `APOD_CONFIG` env var or `apod_wallpaper.conf`.
    """
    proxies, proxy_url = _proxies_from_env_or_config()
    if proxy_url and not _is_proxy_reachable(proxy_url):
        pytest.skip(f"Proxy unreachable: {proxy_url}")

    r = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", proxies=proxies, timeout=10)
    assert r.status_code == 200
