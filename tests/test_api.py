import unittest
import time
import os

from fastapi.testclient import TestClient

from castle.utils import generate_uid
from castle.api.main import fastapi_app
from castle.api.utils import get_api_keys


class APITests(unittest.TestCase):
    def _get_api_key(self) -> str:
        api_keys_path = os.environ["API_KEYS_PATH"]
        valid_api_keys = get_api_keys(api_keys_path=api_keys_path)
        return valid_api_keys[0]


    def setUp(self):
        self.client = TestClient(fastapi_app)
        self.api_key: str = self._get_api_key()
        self.uid: str = generate_uid()
        # Additional setup for your tests

    def test_process_data(self):
        # Define a test case for the `/process/` endpoint
        response = self.client.post(
            "/process/",
            json={"api_key": self.api_key, "start": "start_value", 
                  "stop": "stop_value", "id": 1, "process_uid": self.uid},
        )
        content: dict = response.json()
        self.assertIn("uid", content.keys())
        self.assertIn("url", content.keys())
        self.assertEqual(response.status_code, 200)
        # Additional assertions for the response data, e.g. response.json()

    def test_get_status(self):
        # Define a test case for the `/status/` endpoint
        time.sleep(5)
        response = self.client.get(
            f"/status/{self.api_key}/{self.uid}",
        )
        self.assertEqual(response.status_code, 200)
        # Additional assertions for the response data, e.g. response.json()
        # response_dict: dict = response.json()
        # self.assertEqual(response_dict["status"], "completed")

if __name__ == "__main__":
    unittest.main()
