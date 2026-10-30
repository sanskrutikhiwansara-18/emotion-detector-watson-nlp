"""Unit tests for the EmotionDetection package."""
import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import API_URL, emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Test valid input, invalid input, and service errors."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_emotions_and_dominant_emotion(self, mock_post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.01,
                    "disgust": 0.02,
                    "fear": 0.03,
                    "joy": 0.88,
                    "sadness": 0.06,
                }
            }]
        }
        mock_post.return_value = response

        result = emotion_detector("I am delighted.")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.88)
        self.assertEqual(result["status_code"], 200)
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.args[0], API_URL)

    def test_blank_input_returns_bad_request(self):
        result = emotion_detector("   ")
        self.assertEqual(result["status_code"], 400)
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_service_http_400_is_handled(self, mock_post):
        response = Mock()
        response.status_code = 400
        mock_post.return_value = response

        result = emotion_detector("some text")

        self.assertEqual(result["status_code"], 400)
        self.assertIsNotNone(result["error"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_unexpected_status_is_handled(self, mock_post):
        response = Mock()
        response.status_code = 503
        mock_post.return_value = response

        result = emotion_detector("some text")

        self.assertEqual(result["status_code"], 503)
        self.assertIn("HTTP 503", result["error"])


if __name__ == "__main__":
    unittest.main()
