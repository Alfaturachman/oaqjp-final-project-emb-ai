# oaqjp-final-project-emb-ai

## Final Project - Emotion Detector

An AI-based web application that detects emotions in text using the **Watson NLP Embed library**.

---

## Daftar Isi

- [Gambaran Umum](#gambaran-umum)
- [Arsitektur Proyek](#arsitektur-proyek)
- [Tech Stack](#tech-stack)
- [Struktur Direktori](#struktur-direktori)
- [Prerequisites](#prerequisites)
- [Instalasi & Setup](#instalasi--setup)
- [Task 1 – Clone Repository](#task-1--clone-repository)
- [Task 2 – Emotion Detection Application](#task-2--emotion-detection-application)
- [Task 3 – Format Output](#task-3--format-output)
- [Task 4 – Package EmotionDetection](#task-4--package-emotiondetection)
- [Task 5 – Unit Testing](#task-5--unit-testing)
- [Task 6 – Web Deployment (Flask)](#task-6--web-deployment-flask)
- [Task 7 – Error Handling](#task-7--error-handling)
- [Task 8 – Static Code Analysis (Pylint)](#task-8--static-code-analysis-pylint)
- [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
- [API Endpoint](#api-endpoint)
- [Contoh Output](#contoh-output)
- [Troubleshooting](#troubleshooting)
- [Lisensi](#lisensi)

---

## Gambaran Umum

**Emotion Detector** adalah aplikasi web berbasis AI yang menganalisis teks dan mendeteksi emosi dominan menggunakan **IBM Watson NLP Library**. Aplikasi ini dibangun dengan Python dan Flask, lalu di-deploy sebagai REST API web yang bisa diakses melalui browser.

Emosi yang dideteksi:
| Emosi | Deskripsi |
|-------|-----------|
| 😡 Anger | Kemarahan |
| 🤢 Disgust | Jijik / muak |
| 😨 Fear | Ketakutan |
| 😊 Joy | Kebahagiaan |
| 😢 Sadness | Kesedihan |

---

## Arsitektur Proyek

```
Browser / Client
      │
      ▼  HTTP GET /emotionDetector?textToAnalyze=...
┌─────────────────────┐
│   Flask Server      │  server.py
│   (port 5000)       │
└─────────┬───────────┘
          │  calls
          ▼
┌─────────────────────┐
│  EmotionDetection   │  EmotionDetection/emotion_detection.py
│  Package            │
└─────────┬───────────┘
          │  HTTP POST
          ▼
┌─────────────────────┐
│  IBM Watson NLP     │
│  REST API           │  https://sn-watson-emotion.labs.skills.network
└─────────────────────┘
```

---

## Tech Stack

| Komponen        | Teknologi         | Versi           |
| --------------- | ----------------- | --------------- |
| Language        | Python            | 3.10+           |
| Web Framework   | Flask             | 2.3+            |
| HTTP Client     | Requests          | 2.31+           |
| AI/NLP API      | IBM Watson NLP    | Cloud Endpoint  |
| Testing         | unittest / pytest | built-in / 7.4+ |
| Static Analysis | Pylint            | 3.0+            |

---

## Struktur Direktori

```
emotion_detector/
│
├── EmotionDetection/                  # Python package utama
│   ├── __init__.py                    # Package init, export emotion_detector
│   └── emotion_detection.py           # Core function: emotion_detector()
│
├── templates/
│   └── index.html                     # Frontend UI (HTML/CSS/JS)
│
├── static/                            # (opsional) CSS/JS/gambar statis
│
├── tests/
│   └── test_emotion_detection.py      # Unit tests (unittest)
│
├── server.py                          # Flask web server
├── requirements.txt                   # Python dependencies
├── .pylintrc                          # Pylint configuration
└── README.md                          # Dokumentasi ini
```

---

## Prerequisites

Pastikan sistem kamu memiliki:

- **Python 3.10+** → [Download](https://www.python.org/downloads/)
- **pip** (sudah termasuk di Python 3.x)
- **Git** → [Download](https://git-scm.com/)
- **Koneksi internet** (untuk memanggil Watson NLP API)

Cek versi:

```bash
python --version   # Python 3.10.x atau lebih baru
pip --version
git --version
```

---

## Instalasi & Setup

### 1. Buat virtual environment

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Linux/macOS)
source venv/bin/activate

# Aktifkan (Windows CMD)
venv\Scripts\activate

# Aktifkan (Windows PowerShell)
venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Output yang diharapkan:

```
Successfully installed flask-2.3.x requests-2.31.x pylint-3.0.x pytest-7.4.x
```

---

## Task 1 – Clone Repository

### Langkah-langkah

```bash
# Clone repository ke local machine
git clone https://github.com/<username>/emotion_detector.git

# Masuk ke direktori project
cd emotion_detector

# Lihat struktur direktori
ls -la
```

### Inisialisasi Git (jika membuat dari awal)

```bash
# Inisialisasi repo baru
git init

# Tambahkan semua file
git add .

# Commit pertama
git commit -m "Initial commit: Emotion Detector project"

# Hubungkan ke GitHub
git remote add origin https://github.com/<username>/emotion_detector.git
git branch -M main
git push -u origin main
```

### Verifikasi

```bash
git log --oneline
# Output: abc1234 Initial commit: Emotion Detector project

# Pastikan README.md ada
cat README.md
```

> 📌 **Submit**: URL repository GitHub dalam format  
> `https://github.com/<username>/emotion_detector/blob/main/README.md`

---

## Task 2 – Emotion Detection Application

### Penjelasan

File utama adalah `EmotionDetection/emotion_detection.py`. Fungsi `emotion_detector()` memanggil **Watson NLP Emotion Predict endpoint** via HTTP POST, lalu mengekstrak skor tiap emosi dari respons JSON.

### Kode: `EmotionDetection/emotion_detection.py`

```python
"""
Emotion Detection Module
========================
Uses IBM Watson NLP Library (via Watson NLP REST API) to analyze
text and return emotion scores (anger, disgust, fear, joy, sadness).
"""

import requests
import json


def emotion_detector(text_to_analyse: str) -> dict:
    """
    Analyze the given text and return emotion scores using Watson NLP.

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
    """
    # Guard: blank / whitespace-only input
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

    response = requests.post(url, headers=headers, json=payload)

    # Handle HTTP 400
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
    emotions = response_json["emotionPredictions"][0]["emotion"]

    anger   = emotions.get("anger",   0.0)
    disgust = emotions.get("disgust", 0.0)
    fear    = emotions.get("fear",    0.0)
    joy     = emotions.get("joy",     0.0)
    sadness = emotions.get("sadness", 0.0)

    emotion_scores = {
        "anger": anger, "disgust": disgust,
        "fear": fear, "joy": joy, "sadness": sadness,
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "anger": anger, "disgust": disgust, "fear": fear,
        "joy": joy, "sadness": sadness, "dominant_emotion": dominant_emotion,
    }
```

### Test di Terminal (Activity 2)

```bash
# Masuk ke direktori project
cd emotion_detector

# Buka Python interactive shell
python3

# Di dalam shell Python:
>>> from EmotionDetection.emotion_detection import emotion_detector
>>> result = emotion_detector("I am so happy today!")
>>> print(result)
```

Output yang diharapkan:

```python
{
  'anger': 0.0058, 'disgust': 0.0047, 'fear': 0.0052,
  'joy': 0.9651, 'sadness': 0.0191,
  'dominant_emotion': 'joy'
}
```

---

## Task 3 – Format Output

### Penjelasan

Fungsi `emotion_detector()` sudah diformat untuk mengembalikan dictionary dengan 6 key:

- `anger`, `disgust`, `fear`, `joy`, `sadness` → nilai float antara 0 dan 1
- `dominant_emotion` → string nama emosi dengan skor tertinggi

### Verifikasi Format Output

```bash
python3
```

```python
>>> from EmotionDetection import emotion_detector
>>> result = emotion_detector("I am really mad about this!")
>>> print(type(result))
<class 'dict'>

>>> print(result.keys())
dict_keys(['anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion'])

>>> print(result)
{
  'anger': 0.7423, 'disgust': 0.1049, 'fear': 0.0852,
  'joy': 0.0301, 'sadness': 0.0374,
  'dominant_emotion': 'anger'
}

>>> print(f"Dominant emotion: {result['dominant_emotion']}")
Dominant emotion: anger
```

---

## Task 4 – Package EmotionDetection

### File: `EmotionDetection/__init__.py`

```python
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
```

### Validasi Package di Terminal (Activity 2)

```bash
# Dari root direktori project
python3

>>> import EmotionDetection
>>> print(EmotionDetection.__version__)
1.0.0

>>> from EmotionDetection import emotion_detector
>>> print(emotion_detector)
<function emotion_detector at 0x...>

>>> # Test langsung dari package
>>> result = emotion_detector("I feel disgusted just hearing about this")
>>> print(result['dominant_emotion'])
disgust
```

Atau dengan cara lebih formal:

```bash
python3 -c "
import EmotionDetection
print('Package loaded:', EmotionDetection)
print('Version:', EmotionDetection.__version__)
print('Exports:', EmotionDetection.__all__)
"
```

Output:

```
Package loaded: <module 'EmotionDetection' from '.../EmotionDetection/__init__.py'>
Version: 1.0.0
Exports: ['emotion_detector']
```

> 📌 **Submit**: URL file `__init__.py` di GitHub:  
> `https://github.com/<username>/emotion_detector/blob/main/EmotionDetection/__init__.py`

---

## Task 5 – Unit Testing

### File: `tests/test_emotion_detection.py`

```python
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

    def test_blank_input_returns_none(self):
        """Blank input should return None for all fields."""
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])
        self.assertIsNone(result["anger"])

    def test_return_keys_present(self):
        """Result must contain all required keys."""
        result = emotion_detector("I love this project")
        expected_keys = {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"}
        self.assertEqual(set(result.keys()), expected_keys)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

### Jalankan Unit Tests

```bash
# Menggunakan pytest (direkomendasikan)
python -m pytest tests/test_emotion_detection.py -v

# Menggunakan unittest
python -m unittest tests/test_emotion_detection.py -v
```

Output yang diharapkan:

```
tests/test_emotion_detection.py::TestEmotionDetector::test_anger_statement PASSED
tests/test_emotion_detection.py::TestEmotionDetector::test_blank_input_returns_none PASSED
tests/test_emotion_detection.py::TestEmotionDetector::test_disgust_statement PASSED
tests/test_emotion_detection.py::TestEmotionDetector::test_fear_statement PASSED
tests/test_emotion_detection.py::TestEmotionDetector::test_joy_statement PASSED
tests/test_emotion_detection.py::TestEmotionDetector::test_return_keys_present PASSED
tests/test_emotion_detection.py::TestEmotionDetector::test_sadness_statement PASSED

============================== 7 passed in 4.83s ===============================
```

---

## Task 6 – Web Deployment (Flask)

### File: `server.py`

```python
"""
Emotion Detector – Flask Web Server
=====================================
Routes:
  GET  /                → renders the web UI (index.html)
  GET  /emotionDetector → calls emotion_detector, returns plain-text result
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Query parameter : textToAnalyze (str)
    Returns         : human-readable emotion analysis string, or error message.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = emotion_detector(text_to_analyze)

    # Error handling: blank or invalid input
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again."

    anger    = result["anger"]
    disgust  = result["disgust"]
    fear     = result["fear"]
    joy      = result["joy"]
    sadness  = result["sadness"]
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
```

### Jalankan Server Flask

```bash
# Dari root direktori project
python server.py
```

Output terminal:

```
 * Serving Flask app 'Emotion Detector'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

### Test Deployment

Buka browser dan akses:

- **UI**: `http://localhost:5000/`
- **API langsung**: `http://localhost:5000/emotionDetector?textToAnalyze=I+am+so+happy`

Atau via curl:

```bash
curl "http://localhost:5000/emotionDetector?textToAnalyze=I+am+so+happy+today"
```

Output:

```
For the given statement, the system response is 'anger': 0.0058, 'disgust': 0.0047,
'fear': 0.0052, 'joy': 0.9651 and 'sadness': 0.0191. The dominant emotion is joy.
```

> 📸 **Screenshot**: Simpan screenshot browser sebagai `6b_deployment_test.png`

---

## Task 7 – Error Handling

### Skenario Error

Ketika user mengirim **teks kosong**, aplikasi harus mengembalikan pesan yang jelas alih-alih crash.

### Error Handling di `emotion_detection.py` (status 400)

Bagian kode yang menangani error (sudah diimplementasi di Task 2):

```python
# Guard: blank / whitespace-only input (SEBELUM memanggil API)
if not text_to_analyse or not text_to_analyse.strip():
    return {
        "anger": None, "disgust": None, "fear": None,
        "joy": None, "sadness": None, "dominant_emotion": None,
    }

# ...setelah request API...

# Handle HTTP 400 dari Watson API
if response.status_code == 400:
    return {
        "anger": None, "disgust": None, "fear": None,
        "joy": None, "sadness": None, "dominant_emotion": None,
    }
```

### Error Handling di `server.py`

```python
@app.route("/emotionDetector")
def emotion_detector_route():
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = emotion_detector(text_to_analyze)

    # Jika dominant_emotion None → input tidak valid
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again."    # ← Error handling

    # ... format dan return hasil normal
```

### Test Error Handling

```bash
# Test dengan teks kosong via curl
curl "http://localhost:5000/emotionDetector?textToAnalyze="
# Output: Invalid text! Please try again.

# Test dengan spasi saja
curl "http://localhost:5000/emotionDetector?textToAnalyze=   "
# Output: Invalid text! Please try again.
```

> 📸 **Screenshot**: Simpan screenshot browser yang menampilkan error handling sebagai `7c_error_handling_interface.png`

---

## Task 8 – Static Code Analysis (Pylint)

### Jalankan Pylint

```bash
# Analisis file server.py
pylint server.py

# Analisis seluruh package
pylint server.py EmotionDetection/emotion_detection.py
```

### Target: Skor 10/10

Untuk mendapatkan skor sempurna, pastikan kode memenuhi standar:

- Semua fungsi memiliki docstring
- Nama variabel dan fungsi mengikuti konvensi PEP 8
- Tidak ada baris yang terlalu panjang (>100 karakter per `.pylintrc`)
- Tidak ada import yang tidak digunakan
- Tidak ada variabel yang tidak digunakan

### Contoh Output Pylint (Skor Sempurna)

```
--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

### Tips Memperbaiki Skor Pylint

Jika skor belum sempurna, jalankan:

```bash
# Lihat detail warning/error
pylint server.py --output-format=text

# Fix otomatis dengan autopep8 (opsional)
pip install autopep8
autopep8 --in-place --aggressive server.py
```

Masalah umum dan solusinya:

| Warning Pylint                                       | Solusi                               |
| ---------------------------------------------------- | ------------------------------------ |
| `C0116: Missing function or method docstring`        | Tambahkan docstring ke setiap fungsi |
| `C0301: Line too long`                               | Potong baris menjadi <100 karakter   |
| `W0611: Unused import`                               | Hapus import yang tidak digunakan    |
| `C0103: Variable name doesn't conform to snake_case` | Ganti nama variabel ke snake_case    |

---

## Cara Menjalankan Aplikasi

### Quick Start (5 langkah)

```bash
# 1. Clone / masuk ke direktori
git clone https://github.com/<username>/emotion_detector.git
cd emotion_detector

# 2. Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan Flask server
python server.py

# 5. Buka browser
# http://localhost:5000
```

### Mode Development (dengan auto-reload)

```bash
FLASK_ENV=development FLASK_DEBUG=1 flask --app server run --port 5000
```

### Menjalankan Semua Tests

```bash
# Unit tests
python -m pytest tests/ -v

# Static analysis
pylint server.py EmotionDetection/emotion_detection.py
```

---

## API Endpoint

### `GET /emotionDetector`

Menganalisis teks dan mengembalikan skor emosi dalam format plain-text.

**Query Parameters:**

| Parameter       | Tipe   | Wajib | Deskripsi                 |
| --------------- | ------ | ----- | ------------------------- |
| `textToAnalyze` | string | Ya    | Teks yang akan dianalisis |

**Contoh Request:**

```
GET /emotionDetector?textToAnalyze=I+am+so+happy+today
```

**Contoh Response (200 OK):**

```
For the given statement, the system response is 'anger': 0.0058, 'disgust': 0.0047,
'fear': 0.0052, 'joy': 0.9651 and 'sadness': 0.0191. The dominant emotion is joy.
```

**Error Response (input kosong):**

```
Invalid text! Please try again.
```

---

### `GET /`

Menampilkan antarmuka web utama (HTML/CSS/JS).

---

## Contoh Output

### Input: "I am so happy today!"

```json
{
    "anger": 0.0058,
    "disgust": 0.0047,
    "fear": 0.0052,
    "joy": 0.9651,
    "sadness": 0.0191,
    "dominant_emotion": "joy"
}
```

### Input: "I am really mad about this!"

```json
{
    "anger": 0.7423,
    "disgust": 0.1049,
    "fear": 0.0852,
    "joy": 0.0301,
    "sadness": 0.0374,
    "dominant_emotion": "anger"
}
```

### Input: "" (kosong)

```json
{
    "anger": null,
    "disgust": null,
    "fear": null,
    "joy": null,
    "sadness": null,
    "dominant_emotion": null
}
```

---

## Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'EmotionDetection'`

```bash
# Pastikan kamu berada di root direktori project
pwd
# Harus output: /path/to/emotion_detector

# Jalankan dari direktori yang benar
cd /path/to/emotion_detector
python server.py
```

### Problem: `ConnectionError` saat memanggil Watson API

```bash
# Cek koneksi internet
ping sn-watson-emotion.labs.skills.network

# Cek apakah endpoint merespons
curl -I https://sn-watson-emotion.labs.skills.network
```

### Problem: `Port 5000 already in use`

```bash
# Cari proses yang menggunakan port 5000
lsof -i :5000          # Linux/macOS
netstat -ano | find "5000"  # Windows

# Kill proses tersebut (Linux/macOS)
kill -9 <PID>

# Atau jalankan di port berbeda
python server.py --port 5001
```

### Problem: Pylint score rendah

```bash
# Lihat semua warning detail
pylint server.py --output-format=colorized

# Perbaiki satu per satu berdasarkan output
```

---

## Lisensi

This project is licensed under the MIT License - see the LICENSE file for details

---

_This project is for educational purposes only._
