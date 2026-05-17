"""
Emotion Detection Module
========================
Uses IBM Watson NLP Library (via Watson NLP REST API) to analyze
text and return emotion scores (anger, disgust, fear, joy, sadness).
"""

import requests


def emotion_detector(text_to_analyse: str) -> dict:
    """
    Analyze the given text and return emotion scores using Watson NLP.

    The function calls the Watson NLP Emotion Predict endpoint and maps
    the response into a flat dictionary that also includes the dominant
    emotion (the emotion with the highest score).

    Parameters
    ----------
    text_to_analyse : str
        The raw text to analyse for emotional content.

    Returns
    -------
    dict
        Keys: 'anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion'
        All score values are floats in [0, 1].
        When the input is blank / invalid (HTTP 400), all scores are None
        and dominant_emotion is None.

    Examples
    --------
    >>> result = emotion_detector("I am so happy today!")
    >>> result['dominant_emotion']
    'joy'
    """
    # --- Guard: blank / whitespace-only input ---
    if not text_to_analyse or not text_to_analyse.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    # Watson NLP Emotion Predict endpoint
    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/"
        "NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json",
    }

    payload = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
    except requests.exceptions.RequestException:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    # --- Handle HTTP 400 (blank / invalid input from API perspective) ---
    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    # Parse JSON response
    response_json = response.json()

    # Navigate to emotion scores
    emotions = response_json["emotionPredictions"][0]["emotion"]

    anger   = emotions.get("anger",   0.0)
    disgust = emotions.get("disgust", 0.0)
    fear    = emotions.get("fear",    0.0)
    joy     = emotions.get("joy",     0.0)
    sadness = emotions.get("sadness", 0.0)

    # Determine dominant emotion
    emotion_scores = {
        "anger":   anger,
        "disgust": disgust,
        "fear":    fear,
        "joy":     joy,
        "sadness": sadness,
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "anger":   anger,
        "disgust": disgust,
        "fear":    fear,
        "joy":     joy,
        "sadness": sadness,
        "dominant_emotion": dominant_emotion,
    }
