"""Detect emotions in English text using the IBM Skills Network Watson NLP service."""
from typing import Any, Dict

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze: str) -> Dict[str, Any]:
    """Return emotion scores and the dominant emotion for the supplied text.

    An empty input returns a consistent error response. HTTP 400 responses from
    the service are handled without attempting to parse a missing prediction.
    Network errors are returned as readable error responses instead of crashing.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": 400,
            "error": "Please enter some text to analyze.",
        }

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze.strip()}}

    try:
        response = requests.post(
            API_URL, json=payload, headers=headers, timeout=30
        )
    except requests.RequestException as exc:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": 503,
            "error": f"Emotion service is unavailable: {exc}",
        }

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": 400,
            "error": "The service could not analyze this input. Please try different text.",
        }

    if response.status_code != 200:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": response.status_code,
            "error": f"Emotion service returned HTTP {response.status_code}.",
        }

    try:
        data = response.json()
        prediction = data["emotionPredictions"][0]["emotion"]
        result = {name: float(prediction[name]) for name in EMOTION_NAMES}
    except (ValueError, KeyError, IndexError, TypeError):
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
            "status_code": 502,
            "error": "The emotion service returned an unexpected response.",
        }

    result["dominant_emotion"] = max(
        EMOTION_NAMES, key=lambda emotion: result[emotion]
    )
    result["status_code"] = 200
    result["error"] = None
    return result
