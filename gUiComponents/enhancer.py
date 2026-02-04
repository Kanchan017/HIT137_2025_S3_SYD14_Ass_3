import cv2
class ImageModel:
    """Holds image state and supports undo/redo."""
    def __init__(self, img=None, filename=None):
        self._filename = filename
        self._history = []
        self._idx = -1
        if img is not None:
            self.set_image(img, filename)

    def set_image(self, img, filename=None):
        arr = img.copy()
        # store BGR numpy array
        self._filename = filename or self._filename
        # trim forward history
        if self._idx < len(self._history) - 1:
            self._history = self._history[: self._idx + 1]
        self._history.append(arr)
        self._idx += 1

    def current(self):
        if self._idx >= 0:
            return self._history[self._idx]
        return None

    def undo(self):
        if self._idx > 0:
            self._idx -= 1
            return True
        return False

    def redo(self):
        if self._idx < len(self._history) - 1:
            self._idx += 1
            return True
        return False

    def filename(self):
        return self._filename


class ImageProcessor:
    """Stateless image processing helper using OpenCV."""

    @staticmethod
    def to_grayscale(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def apply_blur(img, ksize=5):
        k = max(1, int(ksize))
        if k % 2 == 0:
            k += 1
        return cv2.GaussianBlur(img, (k, k), 0)

    @staticmethod
    def canny_edges(img, threshold1=100, threshold2=200):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, int(threshold1), int(threshold2))
        # convert single channel to BGR for consistent display
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def adjust_brightness_contrast(img, brightness=0, contrast=1.0):
        # img expected BGR uint8
        beta = int(brightness)
        alpha = float(contrast)
        out = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        return out

    @staticmethod
    def rotate(img, angle):
        if angle % 360 == 0:
            return img.copy()
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(img, M, (w, h))

    @staticmethod
    def flip(img, mode="horizontal"):
        if mode == "horizontal":
            return cv2.flip(img, 1)
        return cv2.flip(img, 0)

    @staticmethod
    def resize_scale(img, scale_percent):
        if scale_percent <= 0:
            return img.copy()
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
