"""Flask web application for the Emotion Detector."""
from flask import Flask, jsonify, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def home():
    """Render the main user interface."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Analyze query-string text and return a readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        message = "Please enter some text to analyze."
        if request.accept_mimetypes.best == "application/json":
            return jsonify({"error": message}), 400
        return render_template("index.html", error=message), 400

    result = emotion_detector(text_to_analyze)
    status_code = result.get("status_code", 200)

    if status_code != 200:
        message = result.get("error") or "Unable to analyze this text."
        if request.accept_mimetypes.best == "application/json":
            return jsonify(result), status_code
        return render_template("index.html", error=message), status_code

    if request.accept_mimetypes.best == "application/json":
        return jsonify(result)

    return render_template("index.html", result=result, submitted_text=text_to_analyze)


@app.get("/health")
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
