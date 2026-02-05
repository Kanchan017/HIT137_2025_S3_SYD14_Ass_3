"""Stateless image processing helpers using OpenCV."""
import cv2
import numpy as np


class ImageProcessor:
    @staticmethod
    def to_grayscale(img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def apply_blur(img: np.ndarray, ksize: int = 5) -> np.ndarray:
        k = max(1, int(ksize))
        if k % 2 == 0:
            k += 1
        return cv2.GaussianBlur(img, (k, k), 0)

    @staticmethod
    def canny_edges(img: np.ndarray, threshold1: int = 100, threshold2: int = 200) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, int(threshold1), int(threshold2))
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def adjust_brightness_contrast(img: np.ndarray, brightness: int = 0, contrast: float = 1.0) -> np.ndarray:
        beta = int(brightness)
        alpha = float(contrast)
        out = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        return out
                
    @staticmethod
    def rotate(img: np.ndarray, angle: float) -> np.ndarray:
        if angle % 360 == 0:
            return img.copy()
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(img, M, (w, h))

    @staticmethod
    def flip(img: np.ndarray, mode: str = "horizontal") -> np.ndarray:
        if mode == "horizontal":
            return cv2.flip(img, 1)
        return cv2.flip(img, 0)

    @staticmethod
    def resize_scale(img: np.ndarray, scale_percent: float) -> np.ndarray:
        if scale_percent <= 0:
            return img.copy()
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
