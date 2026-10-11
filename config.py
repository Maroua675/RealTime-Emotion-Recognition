from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "fer2013_cnn.keras"
CLASSES_PATH = BASE_DIR / "class_names.json"

ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATH = ASSETS_DIR / "logo" / "soai_logo_white.png"
EMOJI_DIR = ASSETS_DIR / "emojis"
BACKGROUND_DIR = ASSETS_DIR / "backgrounds"


# ============================================================
# CAMERA
# ============================================================

CAMERA_INDEX = 0

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


# ============================================================
# EMOTION MODEL
# ============================================================

FACE_SIZE = 48

HISTORY_SIZE = 8


# ============================================================
# UI
# ============================================================

APP_TITLE = "SOAI Béjaïa — AI Emotion Mirror"

UI_UPDATE_INTERVAL = 30


# ============================================================
# SOAI COLORS
# ============================================================

BACKGROUND = "#05090B"

PANEL = "#0A1115"

PANEL_LIGHT = "#101B55"

CYAN = "#00D5E6"

CYAN_DARK = "#007D89"

WHITE = "#FFFFFF"

TEXT_SECONDARY = "#9BA8AD"

GREEN = "#21E6A1"


# Emotion-specific accent colors.
# These are used subtly, while the overall interface remains SOAI-themed.

EMOTION_COLORS = {
    "angry": "#FF5A5F",
    "happy": "#FFD166",
    "neutral": "#00D5E6",
    "sad": "#6EA8FE",
    "surprise": "#C77DFF",
    "fear": "#FF9AA2"
}