from pathlib import Path

import cv2

from PySide6.QtCore import (
    Qt,
    QTimer,
    QRectF
)

from PySide6.QtGui import (
    QImage,
    QPixmap,
    QPainter,
    QPen,
    QColor,
    QFont
)

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QFrame
)


class EmotionMirrorUI(QMainWindow):

    def __init__(
        self,
        camera,
        emotion_engine,
        emoji_dir,
        logo_path,
        config
    ):

        super().__init__()

        self.camera = camera

        self.emotion_engine = emotion_engine

        self.emoji_dir = Path(
            emoji_dir
        )

        self.logo_path = Path(
            logo_path
        )

        self.config = config

        self.current_result = None

        self.current_emoji = None

        self.setup_window()

        self.setup_ui()

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_frame
        )

        self.timer.start(
            self.config.UI_UPDATE_INTERVAL
        )

    # ========================================================
    # WINDOW
    # ========================================================

    def setup_window(self):

        self.setWindowTitle(
            self.config.APP_TITLE
        )

        self.setWindowState(
            Qt.WindowFullScreen
        )

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {self.config.BACKGROUND};
            }}

            QWidget {{
                background: {self.config.BACKGROUND};
                color: {self.config.WHITE};
                font-family: "Segoe UI";
            }}
            """
        )

    # ========================================================
    # MAIN UI
    # ========================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            40,
            25,
            40,
            25
        )

        main_layout.setSpacing(20)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QHBoxLayout()

        self.logo = QLabel()

        if self.logo_path.exists():

            pixmap = QPixmap(
                str(self.logo_path)
            )

            pixmap = pixmap.scaled(
                190,
                100,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.logo.setPixmap(
                pixmap
            )

        else:

            self.logo.setText(
                "SOAI\nBÉJAÏA"
            )

            self.logo.setStyleSheet(
                f"""
                color: {self.config.WHITE};
                font-size: 26px;
                font-weight: 700;
                """
            )

        header.addWidget(
            self.logo
        )

        header.addStretch()

        title = QLabel(
            "AI EMOTION MIRROR"
        )

        title.setStyleSheet(
            f"""
            color: {self.config.CYAN};
            font-size: 24px;
            font-weight: 600;
            letter-spacing: 3px;
            """
        )

        header.addWidget(
            title
        )

        main_layout.addLayout(
            header
        )

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        content = QHBoxLayout()

        content.setSpacing(25)

        # CAMERA
        self.camera_card = self.create_card()

        camera_layout = QVBoxLayout(
            self.camera_card
        )

        camera_title = QLabel(
            "LIVE CAMERA"
        )

        camera_title.setStyleSheet(
            self.title_style()
        )

        camera_layout.addWidget(
            camera_title
        )

        self.camera_label = QLabel()

        self.camera_label.setAlignment(
            Qt.AlignCenter
        )

        self.camera_label.setMinimumSize(
            700,
            450
        )

        self.camera_label.setStyleSheet(
            f"""
            background: #020506;
            border: 1px solid {self.config.CYAN_DARK};
            border-radius: 14px;
            """
        )

        camera_layout.addWidget(
            self.camera_label,
            1
        )

        self.status_label = QLabel(
            "● CAMERA INITIALIZING"
        )

        self.status_label.setStyleSheet(
            f"""
            color: {self.config.TEXT_SECONDARY};
            font-size: 13px;
            padding-top: 5px;
            """
        )

        camera_layout.addWidget(
            self.status_label
        )

        content.addWidget(
            self.camera_card,
            3
        )

        # RIGHT PANEL
        right_panel = self.create_right_panel()

        content.addWidget(
            right_panel,
            1
        )

        main_layout.addLayout(
            content,
            1
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = QHBoxLayout()

        footer_left = QLabel(
            "SOAI • BÉJAÏA"
        )

        footer_left.setStyleSheet(
            f"""
            color: {self.config.TEXT_SECONDARY};
            font-size: 13px;
            letter-spacing: 2px;
            """
        )

        footer.addWidget(
            footer_left
        )

        footer.addStretch()

        footer_right = QLabel(
            "Q  •  EXIT"
        )

        footer_right.setStyleSheet(
            f"""
            color: {self.config.TEXT_SECONDARY};
            font-size: 12px;
            """
        )

        footer.addWidget(
            footer_right
        )

        main_layout.addLayout(
            footer
        )

    # ========================================================
    # RIGHT PANEL
    # ========================================================

    def create_right_panel(self):

        panel = self.create_card()

        layout = QVBoxLayout(
            panel
        )

        # Current emotion title
        title = QLabel(
            "CURRENT EMOTION"
        )

        title.setStyleSheet(
            self.title_style()
        )

        layout.addWidget(
            title
        )

        # Emoji
        self.emoji_label = QLabel(
            "●"
        )

        self.emoji_label.setAlignment(
            Qt.AlignCenter
        )

        self.emoji_label.setMinimumHeight(
            160
        )

        self.emoji_label.setStyleSheet(
            f"""
            color: {self.config.CYAN};
            font-size: 80px;
            """
        )

        layout.addWidget(
            self.emoji_label
        )

        # Emotion name
        self.emotion_label = QLabel(
            "WAITING"
        )

        self.emotion_label.setAlignment(
            Qt.AlignCenter
        )

        self.emotion_label.setStyleSheet(
            f"""
            color: {self.config.WHITE};
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 2px;
            """
        )

        layout.addWidget(
            self.emotion_label
        )

        # Confidence
        self.confidence_label = QLabel(
            "—"
        )

        self.confidence_label.setAlignment(
            Qt.AlignCenter
        )

        self.confidence_label.setStyleSheet(
            f"""
            color: {self.config.CYAN};
            font-size: 20px;
            font-weight: 600;
            """
        )

        layout.addWidget(
            self.confidence_label
        )

        separator = QFrame()

        separator.setFrameShape(
            QFrame.HLine
        )

        separator.setStyleSheet(
            f"""
            color: {self.config.CYAN_DARK};
            """
        )

        layout.addWidget(
            separator
        )

        # Analysis title
        analysis_title = QLabel(
            "EMOTION ANALYSIS"
        )

        analysis_title.setStyleSheet(
            self.title_style()
        )

        layout.addWidget(
            analysis_title
        )

        # Progress bars
        self.bars = {}

        for emotion in self.emotion_engine.class_names:

            row = QVBoxLayout()

            name = QLabel(
                emotion.upper()
            )

            name.setStyleSheet(
                f"""
                color: {self.config.TEXT_SECONDARY};
                font-size: 11px;
                font-weight: 600;
                """
            )

            bar = QProgressBar()

            bar.setRange(
                0,
                100
            )

            bar.setValue(
                0
            )

            bar.setTextVisible(
                False
            )

            color = self.config.EMOTION_COLORS.get(
                emotion,
                self.config.CYAN
            )

            bar.setStyleSheet(
                f"""
                QProgressBar {{
                    background: #11191D;
                    border: none;
                    border-radius: 4px;
                    height: 7px;
                }}

                QProgressBar::chunk {{
                    background: {color};
                    border-radius: 4px;
                }}
                """
            )

            row.addWidget(
                name
            )

            row.addWidget(
                bar
            )

            layout.addLayout(
                row
            )

            self.bars[emotion] = bar

        layout.addStretch()

        return panel

    # ========================================================
    # HELPERS
    # ========================================================

    def create_card(self):

        card = QFrame()

        card.setStyleSheet(
            f"""
            QFrame {{
                background: {self.config.PANEL};
                border: 1px solid #18252A;
                border-radius: 16px;
            }}
            """
        )

        return card

    def title_style(self):

        return f"""
        color: {self.config.CYAN};
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 2px;
        padding-bottom: 6px;
        """

    # ========================================================
    # CAMERA UPDATE
    # ========================================================

    def update_frame(self):

        frame, faces = self.camera.read()

        if frame is None:

            self.status_label.setText(
                "● CAMERA ERROR"
            )

            return

        result = None

        if len(faces) > 0:

            # Select largest face
            face = max(
                faces,
                key=lambda f: f[2] * f[3]
            )

            result = (
                self.emotion_engine.predict(
                    frame,
                    face
                )
            )

            if result:

                self.current_result = result

                self.draw_face_box(
                    frame,
                    face
                )

                self.update_emotion_panel(
                    result
                )

                self.status_label.setText(
                    "● FACE DETECTED • AI ACTIVE"
                )

        else:

            self.emotion_engine.clear_history()

            self.current_result = None

            self.emotion_label.setText(
                "WAITING"
            )

            self.confidence_label.setText(
                "STEP INTO THE FRAME"
            )

            self.emoji_label.setText(
                "●"
            )

            self.emoji_label.setPixmap(
                QPixmap()
            )

            self.status_label.setText(
                "● CAMERA ACTIVE • LOOK AT THE CAMERA"
            )

            for bar in self.bars.values():

                bar.setValue(0)

        # Convert OpenCV frame to Qt
        self.display_frame(
            frame
        )

    # ========================================================
    # FACE BOX
    # ========================================================

    def draw_face_box(
        self,
        frame,
        face
    ):

        x, y, w, h = face

        # Cyan face rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 213, 230),
            3
        )

        # Corner brackets
        length = 25

        color = (
            0,
            213,
            230
        )

        thickness = 5

        # Top-left
        cv2.line(
            frame,
            (x, y),
            (x+length, y),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x, y),
            (x, y+length),
            color,
            thickness
        )

        # Top-right
        cv2.line(
            frame,
            (x+w, y),
            (x+w-length, y),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x+w, y),
            (x+w, y+length),
            color,
            thickness
        )

        # Bottom-left
        cv2.line(
            frame,
            (x, y+h),
            (x+length, y+h),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x, y+h),
            (x, y+h-length),
            color,
            thickness
        )

        # Bottom-right
        cv2.line(
            frame,
            (x+w, y+h),
            (x+w-length, y+h),
            color,
            thickness
        )

        cv2.line(
            frame,
            (x+w, y+h),
            (x+w, y+h-length),
            color,
            thickness
        )

    # ========================================================
    # EMOTION PANEL UPDATE
    # ========================================================

    def update_emotion_panel(
        self,
        result
    ):

        label = result["label"]

        confidence = result["confidence"]

        probabilities = result[
            "probabilities"
        ]

        self.emotion_label.setText(
            label.upper()
        )

        self.confidence_label.setText(
            f"{confidence:.0%} CONFIDENCE"
        )

        # Load emoji
        emoji_path = (
            self.emoji_dir
            / f"{label}.png"
        )

        if emoji_path.exists():

            pixmap = QPixmap(
                str(emoji_path)
            )

            pixmap = pixmap.scaled(
                170,
                170,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.emoji_label.setText("")

            self.emoji_label.setPixmap(
                pixmap
            )

        # Update bars
        for emotion, bar in self.bars.items():

            probability = probabilities.get(
                emotion,
                0
            )

            bar.setValue(
                int(probability * 100)
            )

    # ========================================================
    # DISPLAY CAMERA FRAME
    # ========================================================

    def display_frame(
        self,
        frame
    ):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        h, w, channels = rgb.shape

        bytes_per_line = (
            channels * w
        )

        image = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(
            image
        )

        pixmap = pixmap.scaled(
            self.camera_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.camera_label.setPixmap(
            pixmap
        )

    # ========================================================
    # KEYBOARD
    # ========================================================

    def keyPressEvent(
        self,
        event
    ):

        if event.key() == Qt.Key_Q:

            self.close()

        elif event.key() == Qt.Key_Escape:

            self.close()

        else:

            super().keyPressEvent(
                event
            )

    # ========================================================
    # CLOSE
    # ========================================================

    def closeEvent(
        self,
        event
    ):

        self.timer.stop()

        self.camera.release()

        event.accept()