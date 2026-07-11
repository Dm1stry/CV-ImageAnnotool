from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import numpy as np


class ImageCanvas(QLabel):
    """QLabel-based replacement for a cv2.namedWindow/imshow/setMouseCallback window.

    Mouse/wheel events are translated to the same (event, x, y, flags, param)
    shape cv2.setMouseCallback used, so existing callback logic stays unchanged.

    The widget is shown at a capped display size (max_width x max_height) even
    when the source image is much larger, to keep the window small; mouse
    coordinates are scaled back up to source-image space before being handed
    to the callback, so callers keep working in source-image pixels.
    """

    def __init__(self, width, height, max_width=900, max_height=650, parent=None):
        super().__init__(parent)
        scale = min(max_width / width, max_height / height, 1.0)
        self.display_width = max(1, round(width * scale))
        self.display_height = max(1, round(height * scale))
        self.scale_x = width / self.display_width
        self.scale_y = height / self.display_height
        self.setFixedSize(self.display_width, self.display_height)
        self._callback = None

    def setMouseCallback(self, callback):
        self._callback = callback

    def imshow(self, image):
        image = np.ascontiguousarray(image)
        if image.shape[1] != self.display_width or image.shape[0] != self.display_height:
            image = cv2.resize(image, (self.display_width, self.display_height))
        h, w = image.shape[:2]
        qimg = QImage(image.data, w, h, image.strides[0], QImage.Format_BGR888).copy()
        self.setPixmap(QPixmap.fromImage(qimg))

    def _emit(self, event, x, y, flags):
        if self._callback is not None:
            self._callback(event, round(x * self.scale_x), round(y * self.scale_y), flags, None)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._emit(cv2.EVENT_LBUTTONDOWN, event.pos().x(), event.pos().y(), 0)
        elif event.button() == Qt.RightButton:
            self._emit(cv2.EVENT_RBUTTONDOWN, event.pos().x(), event.pos().y(), 0)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._emit(cv2.EVENT_LBUTTONUP, event.pos().x(), event.pos().y(), 0)
        elif event.button() == Qt.RightButton:
            self._emit(cv2.EVENT_RBUTTONUP, event.pos().x(), event.pos().y(), 0)

    def mouseMoveEvent(self, event):
        self._emit(cv2.EVENT_MOUSEMOVE, event.pos().x(), event.pos().y(), 0)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self._emit(cv2.EVENT_MOUSEWHEEL, event.pos().x(), event.pos().y(), delta)
