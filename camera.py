import cv2


class Camera:

    def __init__(
        self,
        index=0,
        width=1280,
        height=720
    ):
        self.index = index

        self.width = width
        self.height = height

        self.cap = None

        self.cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades
            + "haarcascade_frontalface_default.xml"
        )

        if self.cascade.empty():
            raise RuntimeError(
                "Could not load Haar Cascade face detector."
            )

    def start(self):

        self.cap = cv2.VideoCapture(
            self.index,
            cv2.CAP_DSHOW
        )

        if not self.cap.isOpened():
            raise RuntimeError(
                "Could not open camera."
            )

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.width
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.height
        )

        ok, frame = self.cap.read()

        if not ok:
            self.release()

            raise RuntimeError(
                "Camera opened but no frame was received."
            )

        print("Camera is working.")

    def read(self):

        if self.cap is None:
            return None, []

        ok, frame = self.cap.read()

        if not ok:
            return None, []

        # Mirror the camera
        frame = cv2.flip(frame, 1)

        # Resize to a predictable size
        frame = cv2.resize(
            frame,
            (1280, 720)
        )

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(80, 80)
        )

        return frame, faces

    def release(self):

        if self.cap is not None:

            self.cap.release()

            self.cap = None