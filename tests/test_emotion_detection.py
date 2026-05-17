"""
Unit Tests – Emotion Detector
==============================
Tests the emotion_detector function with five sample sentences, each
dominated by a specific emotion, plus a blank-input guard test.

Run:
    python -m pytest tests/test_emotion_detection.py -v
    # or
    python -m unittest tests/test_emotion_detection.py -v
"""

import unittest
from EmotionDetection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Unit tests for the emotion_detector function."""

    # ------------------------------------------------------------------
    # Happy-path tests – one for each dominant emotion
    # ------------------------------------------------------------------

    def test_joy_statement(self):
        """'I am glad this happened' should produce joy as dominant."""
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_anger_statement(self):
        """'I am really mad about this' should produce anger as dominant."""
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_disgust_statement(self):
        """'I feel disgusted just hearing about this' should produce disgust."""
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sadness_statement(self):
        """'I am so sad about this' should produce sadness as dominant."""
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_fear_statement(self):
        """'I am really afraid that this will happen' should produce fear."""
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result["dominant_emotion"], "fear")

    # ------------------------------------------------------------------
    # Error-handling test – blank input
    # ------------------------------------------------------------------

    def test_blank_input_returns_none(self):
        """Blank input should return None for all fields."""
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])
        self.assertIsNone(result["anger"])
        self.assertIsNone(result["disgust"])
        self.assertIsNone(result["fear"])
        self.assertIsNone(result["joy"])
        self.assertIsNone(result["sadness"])

    # ------------------------------------------------------------------
    # Schema tests – validate return structure
    # ------------------------------------------------------------------

    def test_return_keys_present(self):
        """Result must contain all required keys."""
        result = emotion_detector("I love this project")
        expected_keys = {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_scores_are_floats(self):
        """Non-blank input must return float scores."""
        result = emotion_detector("I love this project")
        for key in ("anger", "disgust", "fear", "joy", "sadness"):
            self.assertIsInstance(result[key], float, f"{key} should be float")


if __name__ == "__main__":
    unittest.main(verbosity=2)
