import sys

from PySide6.QtWidgets import QApplication

import config

from camera import Camera
from emotion_engine import EmotionEngine
from ui import EmotionMirrorUI


def main():

    print("Starting SOAI Béjaïa Emotion Mirror...")

    # --------------------------------------------------------
    # Camera
    # --------------------------------------------------------

    camera = Camera(
        index=config.CAMERA_INDEX,
        width=config.CAMERA_WIDTH,
        height=config.CAMERA_HEIGHT
    )

    camera.start()

    # --------------------------------------------------------
    # AI emotion engine
    # --------------------------------------------------------

    emotion_engine = EmotionEngine(
        model_path=config.MODEL_PATH,
        classes_path=config.CLASSES_PATH,
        history_size=config.HISTORY_SIZE
    )

    # --------------------------------------------------------
    # Qt application
    # --------------------------------------------------------

    app = QApplication(
        sys.argv
    )

    window = EmotionMirrorUI(
        camera=camera,
        emotion_engine=emotion_engine,
        emoji_dir=config.EMOJI_DIR,
        logo_path=config.LOGO_PATH,
        config=config
    )

    window.showFullScreen()

    print("Application running.")
    print("Press Q or ESC to exit.")

    exit_code = app.exec()

    camera.release()

    sys.exit(
        exit_code
    )


if __name__ == "__main__":
    main()