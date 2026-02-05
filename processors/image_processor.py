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
 
 