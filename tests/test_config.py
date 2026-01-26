import unittest
from pathlib import Path
from apod_wallpaper.config import Config


class TestConfigFromFile(unittest.TestCase):
    def test_loads_existing_conf(self):
        conf_path = Path.cwd() / "apod_wallpaper.conf"
        cfg = Config.from_file(conf_path)
        self.assertTrue(cfg.api_key)
        self.assertTrue(cfg.apod_url)
        self.assertTrue(cfg.download_path)
        self.assertTrue(cfg.def_wallpaper_style)


if __name__ == '__main__':
    unittest.main()
