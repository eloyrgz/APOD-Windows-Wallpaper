import unittest
from unittest.mock import patch, Mock
import tempfile
from pathlib import Path

from apod_wallpaper import wallpaper


class TestWallpaper(unittest.TestCase):
    def test_human_readable_size(self):
        self.assertIn('bytes', wallpaper.human_readable_size(10))
        self.assertIn('KB', wallpaper.human_readable_size(2048))

    @patch('apod_wallpaper.wallpaper.Image')
    @patch('apod_wallpaper.api_client.dispatch_http_get')
    def test_download_image(self, mock_dispatch, mock_image_module):
        # Mock response from dispatch_http_get
        mock_resp = Mock()
        mock_resp.content = b'PNGDATA'
        mock_resp.headers = {'content-length': '6'}
        mock_dispatch.return_value = mock_resp

        # Mock Image.open(...).save to write a file
        mock_image = Mock()

        def fake_save(path, fmt):
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'wb') as f:
                f.write(b'')

        mock_image.open.return_value.save.side_effect = fake_save
        mock_image_module.open.return_value = mock_image.open.return_value

        with tempfile.TemporaryDirectory() as td:
            target = wallpaper.download_image('http://example.com/image.jpg', Path(td), proxies=None)
            self.assertTrue(str(target).endswith('.bmp'))

    def test_set_windows_wallpaper_registry_calls(self):
        import tempfile
        from pathlib import Path
        mock_api = Mock()
        mock_con = Mock()
        mock_gui = Mock()
        # provide constants expected by the function
        mock_con.HKEY_CURRENT_USER = 'HKCU'
        mock_con.KEY_SET_VALUE = 'KEY_SET_VALUE'
        mock_con.SPI_SETDESKWALLPAPER = 20
        mock_con.REG_SZ = 'REG_SZ'

        with patch('apod_wallpaper.wallpaper.win32api', mock_api), \
             patch('apod_wallpaper.wallpaper.win32con', mock_con), \
             patch('apod_wallpaper.wallpaper.win32gui', mock_gui):
            # create a temporary bmp file
            with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as f:
                path = Path(f.name)
            try:
                result = wallpaper.set_windows_wallpaper(path, 1)
                self.assertTrue(result)
                mock_api.RegOpenKeyEx.assert_called()
                # WallpaperStyle and TileWallpaper should be set
                mock_api.RegSetValueEx.assert_any_call(mock_api.RegOpenKeyEx.return_value, 'WallpaperStyle', 0, mock_con.REG_SZ, wallpaper.styles[1])
                mock_api.RegSetValueEx.assert_any_call(mock_api.RegOpenKeyEx.return_value, 'TileWallpaper', 0, mock_con.REG_SZ, wallpaper.TILE_WALLPAPER)
                mock_gui.SystemParametersInfo.assert_called_with(mock_con.SPI_SETDESKWALLPAPER, str(path), 1 + 2)
            finally:
                try:
                    path.unlink()
                except Exception:
                    pass


if __name__ == '__main__':
    unittest.main()
