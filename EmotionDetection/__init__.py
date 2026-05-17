"""
EmotionDetection Package
========================
Exposes the emotion_detector function at the top-level package namespace.

Usage
-----
    from EmotionDetection import emotion_detector

    result = emotion_detector("I love coding!")
    print(result)
"""

from .emotion_detection import emotion_detector

__all__ = ["emotion_detector"]
__version__ = "1.0.0"
