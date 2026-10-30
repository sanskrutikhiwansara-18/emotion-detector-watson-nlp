# Emotion Detector — Watson NLP + Flask

A Flask web application that calls the IBM Skills Network Watson NLP emotion model to estimate **anger, disgust, fear, joy, and sadness**, and identifies the dominant emotion.

## Project structure

```text
emotion_detector_complete/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── templates/
│   └── index.html
├── tests/
│   ├── test_emotion_detection.py
│   └── test_server.py
├── server.py
├── requirements.txt
└── README.md
```

## 1. Set up

Python 3.10 or newer is recommended.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or run `python -m pip install -r requirements.txt` using your chosen Python environment.

### macOS/Linux or Skills Network terminal

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Test the package

Run from the project root (the folder containing `server.py`):

```bash
python -c "from EmotionDetection import emotion_detector; print('EmotionDetection package imported successfully')"
python -m unittest discover -s tests -v
```

The unit tests mock the external service, so they do not need network access. A successful test run ends with `OK`.

## 3. Run the web application

```bash
python server.py
```

Open `http://127.0.0.1:5000` in your browser. Enter text and click **Analyze emotions**. The live emotion analysis requires internet access and availability of the IBM Skills Network service.

Useful endpoints:
- `GET /` — web interface
- `GET /emotionDetector?textToAnalyze=I%20am%20happy` — HTML result
- `GET /health` — health check
- Add `Accept: application/json` to `/emotionDetector` for JSON output.

## 4. Static analysis

Run:

```bash
pylint server.py
pylint EmotionDetection/emotion_detection.py
pylint EmotionDetection/__init__.py
```

Pylint scores depend on the installed version and its enabled rules. Review any reported issues rather than claiming a perfect score without checking the actual terminal output.

## 5. Screenshots required by the course

After launching the app in your browser, capture the real running application and save it as `6b_deployment_test.png`. Then submit blank input and capture the displayed validation message as `7c_error_handling_interface.png`. Do not submit placeholder or fabricated screenshots.

## 6. GitHub submission

Create a **public** GitHub repository, for example `emotion-detector-watson-nlp`, upload the project files, and check that the README and `EmotionDetection/__init__.py` are publicly accessible. In the assignment, submit the actual URLs of those files from your own repository; do not use a URL until you have pushed the files.

## Notes

- The emotion model is a remote service, so live requests may fail if the service is unavailable, network access is blocked, or the service contract changes.
- Unit tests use mocks to test the application's behavior consistently without depending on the remote model.
- Model scores are estimates and should not be treated as psychological or clinical assessments.
