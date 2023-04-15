from unittest import mock, TestCase
import unittest.main as unittest_main
from unittest.mock import MagicMock
import json
from django.conf import settings
from django.core.files.storage import default_storage
from app.services import join_results, get_gpx_file

class TestJoinResults(TestCase):

    def setUp(self):
        self.mock_open = MagicMock()
        default_storage.open = self.mock_open

        self.test_json_data_1 = {"key1": "value1"}
        self.test_json_data_2 = {"key2": "value2"}

    def test_join_results(self):
        path_mapping = {
            "2021": ["race1", "race2"],
            "2022": ["race1"]
        }

        file1 = MagicMock()
        file1.__enter__.return_value = file1
        file1.read.return_value = json.dumps(self.test_json_data_1)

        file2 = MagicMock()
        file2.__enter__.return_value = file2
        file2.read.return_value = json.dumps(self.test_json_data_2)

        file3 = MagicMock()
        file3.__enter__.return_value = file3
        file3.read.return_value = json.dumps(self.test_json_data_1)
        def mock_exists(file_path):
            return file_path in ["2021race1.json", "2021race2.json", "2022race1.json"]

        default_storage.exists = MagicMock(side_effect=mock_exists)
        self.mock_open.side_effect = [file1, file2, file3]
        expected_results = {
            "2021": {
                "race1": self.test_json_data_1,
                "race2": self.test_json_data_2,
            },
            "2022": {
                "race1": self.test_json_data_1,
            },
        }

        results = join_results(path_mapping)
        self.assertEqual(results, expected_results)

    def test_join_results_no_files(self):
        path_mapping = {
            "2021": ["race1", "race2"],
            "2022": ["race1"]
        }
        default_storage.exists = MagicMock(return_value=False)
        expected_results = {
            "2021": {},
            "2022": {},
        }

        results = join_results(path_mapping)
        self.assertEqual(results, expected_results)


class GetGpxFileTests(TestCase):
    @mock.patch("app.services.BytesIO")
    @mock.patch("app.services.requests")
    def test_get_gpx_file_ultra(self, mock_requests, mock_BytesIO):
        mock_response = mock.MagicMock()
        mock_response.content = b"ultra_content"
        mock_requests.get.return_value = mock_response
        result = get_gpx_file("ultra")

        mock_requests.get.assert_called_once_with(settings.ULTRA_GPX_LINK)
        mock_BytesIO.assert_called_once_with(mock_response.content)
        self.assertEqual(result, mock_BytesIO.return_value)

    @mock.patch("app.services.BytesIO")
    @mock.patch("app.services.requests")
    def test_get_gpx_file_sky(self, mock_requests, mock_BytesIO):
        mock_response = mock.MagicMock()
        mock_response.content = b"sky_content"
        mock_requests.get.return_value = mock_response
        result = get_gpx_file("sky")

        mock_requests.get.assert_called_once_with(settings.SKY_GPX_LINK)
        mock_BytesIO.assert_called_once_with(mock_response.content)
        self.assertEqual(result, mock_BytesIO.return_value)

    @mock.patch("app.services.BytesIO")
    @mock.patch("app.services.requests")
    def test_get_gpx_file_unknown_race(self, mock_requests, mock_BytesIO):
        result = get_gpx_file("unknown")

        mock_requests.get.assert_not_called()
        mock_BytesIO.assert_not_called()
        self.assertIsNone(result)



if __name__ == "__main__":
    unittest_main()
