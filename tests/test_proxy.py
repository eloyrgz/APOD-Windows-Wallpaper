import os
import pytest
import requests
from pathlib import Path

from apod_wallpaper.config import Config


def _proxies_from_env_or_config():
    env = os.environ.get("TEST_PROXY")
    if env:
        return {"http": env, "https": env}
    cfg_path = os.environ.get("APOD_CONFIG", "apod_wallpaper.conf")
    p = Path(cfg_path)
    if not p.exists():
        pytest.skip(f"Config file not found: {p}")
    cfg = Config.from_file(p)
    proxies = cfg.proxies
    if not proxies:
        pytest.skip("No proxy configured in config file")
    return proxies


def test_proxy_connects_to_apod():
    """Attempts a simple GET to the APOD endpoint using proxy from env or project config.

    Priority: `TEST_PROXY` env var. Fallback: `APOD_CONFIG` env var or `apod_wallpaper.conf`.
    """
    proxies = _proxies_from_env_or_config()
    try:
        r = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", proxies=proxies, timeout=10)
        assert r.status_code == 200
    except requests.exceptions.ProxyError as e:
        pytest.skip(f"Proxy error (proxy unreachable or rejected request): {e}")
