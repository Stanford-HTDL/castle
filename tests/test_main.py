import unittest

from fastapi.testclient import TestClient

from api.main import app


class MyApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key: str = "valid_api_key"
        self.uid: str = "098h230fb"
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
        response = self.client.get(
            f"/status/{self.api_key}/{self.uid}",
        )
        self.assertEqual(response.status_code, 200)
        # Additional assertions for the response data, e.g. response.json()

if __name__ == "__main__":
    unittest.main()
