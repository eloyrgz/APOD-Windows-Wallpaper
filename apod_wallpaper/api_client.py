
import logging
from typing import Optional
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ProxyError

log = logging.getLogger(__name__)

# Suppress InsecureRequestWarning when verify=False is used intentionally
warnings.simplefilter('ignore', InsecureRequestWarning)


def dispatch_http_get(url: str, proxies: Optional[dict] = None, timeout: int = 30) -> Optional[requests.Response]:
    try:
        log.info("GET %s", url)
        r = requests.get(url, proxies=proxies, verify=False, timeout=timeout)
        r.raise_for_status()
        return r
    except ProxyError as e:
        log.warning("Proxy error while connecting to %s: %s — retrying without proxy", url, e)
        try:
            r = requests.get(url, verify=False, timeout=timeout)
            r.raise_for_status()
            return r
        except Exception as e2:
            log.error("HTTP GET error after retry without proxy: %s", e2)
            return None
    except Exception as e:
        log.error("HTTP GET error: %s", e)
        return None


def get_apod_json(apod_url: str, api_key: str, proxies: Optional[dict] = None) -> Optional[dict]:
    url = f"{apod_url}concept_tags=True&api_key={api_key}"
    r = dispatch_http_get(url, proxies=proxies)
    if r is None:
        return None
    try:
        return r.json()
    except ValueError:
        log.error("Failed to parse JSON response from APOD")
        return None
