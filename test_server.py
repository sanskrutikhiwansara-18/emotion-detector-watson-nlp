"""Flask route tests."""
import unittest
from unittest.mock import patch

from server import app


class ServerTests(unittest.TestCase):
    """Test the web interface and its input validation."""

    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emotion Detector", response.data)

    def test_blank_input_returns_400(self):
        response = self.client.get("/emotionDetector?textToAnalyze=%20%20")
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter some text", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    @patch("server.emotion_detector")
    def test_valid_input_renders_result(self, mock_detector):
        mock_detector.return_value = {
            "anger": 0.01, "disgust": 0.02, "fear": 0.03,
            "joy": 0.88, "sadness": 0.06,
            "dominant_emotion": "joy", "status_code": 200, "error": None,
        }
        response = self.client.get("/emotionDetector?textToAnalyze=I%20am%20happy")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Joy", response.data)


if __name__ == "__main__":
    unittest.main()
