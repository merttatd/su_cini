"""Lightweight, vector-drawn hearts for the goal celebration."""
import math

from PyQt6.QtCore import QPointF, Qt, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget


class KissHearts(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._progress = 0.0
        self.origin = QPointF()
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    def set_progress(self, value):
        self._progress = value
        self.update()

    progress = pyqtProperty(float, fget=lambda self: self._progress, fset=set_progress)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        heart = QPainterPath()
        heart.moveTo(0, 5)
        heart.cubicTo(-18, -6, -8, -18, 0, -9)
        heart.cubicTo(8, -18, 18, -6, 0, 5)
        for index in range(9):
            t = (self._progress - index * 0.055) / 0.56
            if not 0 < t < 1:
                continue
            direction = -1 if index % 2 else 1
            x = self.origin.x() + direction * (30 + index * 10) * t
            y = self.origin.y() - (85 + index * 9) * t
            painter.save()
            painter.translate(x, y)
            painter.rotate(direction * 18 * t)
            scale = (0.55 + 1.35 * math.sin(math.pi * t)) * (1 if index else 1.5)
            painter.scale(scale, scale)
            color = QColor("#FF6099" if index % 2 else "#F43F7F")
            color.setAlphaF(min(1.0, t * 8) * (1 - t))
            painter.setBrush(color)
            painter.drawPath(heart)
            painter.restore()
        painter.end()
