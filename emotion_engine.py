import json
from collections import deque

import cv2
import numpy as np
import tensorflow as tf


class EmotionEngine:

    def __init__(
        self,
        model_path,
        classes_path,
        history_size=8
    ):

        print("Loading emotion model...")

        self.model = tf.keras.models.load_model(
            model_path
        )

        with open(
            classes_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.class_names = json.load(f)

        self.history = deque(
            maxlen=history_size
        )

        print(
            "Model loaded. Classes:",
            self.class_names
        )

    def predict(self, frame, face):

        x, y, w, h = face

        # Crop face
        face_image = frame[
            y:y+h,
            x:x+w
        ]

        if face_image.size == 0:
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(
            face_image,
            cv2.COLOR_BGR2GRAY
        )

        # Resize to FER2013 input
        gray = cv2.resize(
            gray,
            (48, 48)
        )

        # Prepare TensorFlow input
        input_image = gray.reshape(
            1,
            48,
            48,
            1
        ).astype("float32")

        # IMPORTANT:
        # Keep this consistent with the preprocessing
        # used when your CNN was trained.
        #
        # If your training used x / 255.0,
        # change this to:
        #
        # input_image = input_image / 255.0

        prediction = self.model(
            input_image,
            training=False
        ).numpy()[0]

        # Temporal smoothing
        self.history.append(
            prediction
        )

        average = np.mean(
            self.history,
            axis=0
        )

        index = int(
            np.argmax(average)
        )

        label = self.class_names[index]

        confidence = float(
            average[index]
        )

        return {
            "label": label,
            "confidence": confidence,
            "probabilities": {
                name: float(prob)
                for name, prob in zip(
                    self.class_names,
                    average
                )
            }
        }

    def clear_history(self):

        self.history.clear()