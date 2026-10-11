# 🎭 Emotion Mirror — Real-Time Facial Emotion Recognition

Emotion Mirror is a computer vision project that detects facial expressions through a webcam and predicts the corresponding emotion using a trained deep-learning model. It presents the prediction through an interactive interface with emotion emojis.

## ✨ Features

- Real-time webcam input
- Facial emotion prediction using a trained CNN
- Visual emotion feedback using emojis
- Modular Python implementation

## 🧠 Emotions

- Angry 😠
- Fear 😨
- Happy 😄
- Neutral 😐
- Sad 😢
- Surprise 😲

## 🛠️ Tech Stack

- Python
- TensorFlow / Keras
- OpenCV
- Computer Vision
- Convolutional Neural Networks (CNN)

## 📁 Project Structure

```text
emotion_mirror/
├── assets/
│   ├── emojis/
│   └── logo/
├── app.py
├── camera.py
├── class_names.json
├── config.py
├── emotion_engine.py
├── fer2013_cnn.keras
├── requirements.txt
└── ui.py
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/emotion-mirror.git
cd emotion-mirror
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Allow webcam access if prompted by your operating system.

## 📌 Notes

- A compatible webcam is required.
- The trained model must be available at the path expected by the application.
- Predictions may be affected by lighting, camera quality, and facial variations.

## 👩‍💻 Author

Developed as a computer vision and deep-learning project.

