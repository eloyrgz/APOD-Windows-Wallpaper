import unittest
from unittest.mock import patch, Mock

from apod_wallpaper import api_client


class TestApiClient(unittest.TestCase):
    @patch('apod_wallpaper.api_client.requests.get')
    def test_get_apod_json_success(self, mock_get):
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {'media_type': 'image'}
        mock_get.return_value = mock_resp

        result = api_client.get_apod_json('http://example.com/', 'KEY')
        self.assertIsInstance(result, dict)

    @patch('apod_wallpaper.api_client.requests.get')
    def test_get_apod_json_failure(self, mock_get):
        mock_get.side_effect = Exception('network')
        result = api_client.get_apod_json('http://example.com/', 'KEY')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
