#holds image state and supports undo/redo.
from typing import Optional
import numpy as np

class ImageModel:
    def __init__(self, img: Optional[np.ndarray] = None, filename: Optional[str] = None):
        self._filename = filename
        self._history = []
        self._idx = -1
        if img is not None:
            self.set_image(img, filename)

    def set_image(self, img: np.ndarray, filename: Optional[str] = None):
        arr = img.copy()
        self._filename = filename or self._filename
        if self._idx < len(self._history) - 1:
            self._history = self._history[: self._idx + 1]
        self._history.append(arr)
        self._idx += 1

    def current(self) -> Optional[np.ndarray]:
        if self._idx >= 0:
            return self._history[self._idx]
        return None

    def undo(self) -> bool:
        if self._idx > 0:
            self._idx -= 1
            return True
        return False

    def redo(self) -> bool:
        if self._idx < len(self._history) - 1:
            self._idx += 1
            return True
        return False

    def filename(self) -> Optional[str]:
        return self._filename
