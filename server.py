"""
Emotion Detector – Flask Web Server
=====================================
Exposes two routes:
  GET  /           → renders the web UI (index.html)
  GET  /emotionDetector → calls emotion_detector and returns a plain-text result
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Query parameter : text_to_analyze (str)
    Returns         : human-readable emotion analysis string, or an error
                      message when the input is blank.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")

    result = emotion_detector(text_to_analyze)

    # Error handling: blank or invalid input
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again."

    anger   = result["anger"]
    disgust = result["disgust"]
    fear    = result["fear"]
    joy     = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]

    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )

    return response_text


@app.route("/")
def render_index_page():
    """Serve the main HTML interface."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
