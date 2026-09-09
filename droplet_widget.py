from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
)
from PyQt6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
)
from PyQt6.QtWidgets import QWidget


class DropletWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mood = "normal"
        self.rotation = 0.0

        # Karakter çiziminin dikey konumu.
        # Pencerenin kendisini hareket ettirmiyoruz.
        self._bob_offset = 0.0

        self.setFixedSize(150, 170)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.create_bob_animation()

    def create_bob_animation(self) -> None:
        self.bob_animation = QPropertyAnimation(
            self,
            b"bobOffset"
        )

        self.bob_animation.setDuration(1600)

        self.bob_animation.setStartValue(0.0)
        self.bob_animation.setKeyValueAt(0.5, -5.0)
        self.bob_animation.setEndValue(0.0)

        self.bob_animation.setLoopCount(-1)

        self.bob_animation.setEasingCurve(
            QEasingCurve.Type.InOutSine
        )

    def showEvent(self, event) -> None:
        self.bob_animation.start()
        super().showEvent(event)

    def hideEvent(self, event) -> None:
        self.bob_animation.stop()
        super().hideEvent(event)

    def get_bob_offset(self) -> float:
        return self._bob_offset

    def set_bob_offset(self, value: float) -> None:
        self._bob_offset = value
        self.update()

    bobOffset = pyqtProperty(
        float,
        fget=get_bob_offset,
        fset=set_bob_offset
    )

    def set_mood(self, mood: str) -> None:
        self.mood = mood
        self.update()

    def set_rotation(self, degrees: float) -> None:
        self.rotation = degrees
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.rotation)
        painter.translate(-self.width() / 2, -self.height() / 2)

        # Sadece çizimi hareket ettirir.
        # QWidget ve pencere pozisyonu sabit kalır.
        painter.translate(
            0,
            self._bob_offset
        )

        self.draw_shadow(painter)
        self.draw_body(painter)
        self.draw_highlight(painter)
        self.draw_face(painter)
        self.draw_blush(painter)

        painter.end()

    def draw_shadow(self, painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 45))

        painter.drawEllipse(
            33,
            147,
            84,
            13
        )

    def draw_body(self, painter: QPainter) -> None:
        droplet_path = QPainterPath()

        droplet_path.moveTo(75, 10)

        droplet_path.cubicTo(
            64, 37,
            31, 65,
            31, 104
        )

        droplet_path.cubicTo(
            31, 137,
            50, 151,
            75, 151
        )

        droplet_path.cubicTo(
            100, 151,
            119, 137,
            119, 104
        )

        droplet_path.cubicTo(
            119, 65,
            86, 37,
            75, 10
        )

        droplet_path.closeSubpath()

        painter.setBrush(
            QColor("#68C8FF")
        )

        painter.setPen(
            QPen(
                QColor("#2A91D1"),
                3
            )
        )

        painter.drawPath(
            droplet_path
        )

    def draw_highlight(self, painter: QPainter) -> None:
        highlight_path = QPainterPath()

        highlight_path.moveTo(
            53,
            51
        )

        highlight_path.cubicTo(
            44, 63,
            40, 80,
            41, 92
        )

        highlight_pen = QPen(
            QColor(
                255,
                255,
                255,
                155
            ),
            6
        )

        highlight_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            highlight_pen
        )

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawPath(
            highlight_path
        )

    def draw_face(self, painter: QPainter) -> None:
        face_color = QColor("#18354A")

        face_pen = QPen(
            face_color,
            4
        )

        face_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            face_pen
        )

        painter.setBrush(
            face_color
        )

        if self.mood == "kiss":
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawArc(50, 92, 18, 14, 0, 180 * 16)
            painter.drawArc(82, 92, 18, 14, 0, 180 * 16)
            lips = QPainterPath()
            lips.moveTo(72, 111)
            lips.cubicTo(87, 108, 86, 115, 77, 116)
            lips.cubicTo(87, 117, 86, 124, 72, 121)
            painter.setPen(QPen(QColor("#D94179"), 3))
            painter.drawPath(lips)

        elif self.mood == "happy":
            self.draw_happy_face(painter)

        elif self.mood == "worried":
            self.draw_worried_face(painter)

        elif self.mood == "dramatic":
            self.draw_dramatic_face(painter)

        else:
            self.draw_normal_face(painter)

    def draw_normal_face(self, painter: QPainter) -> None:
        painter.drawEllipse(
            53,
            94,
            8,
            10
        )

        painter.drawEllipse(
            89,
            94,
            8,
            10
        )

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawArc(
            61,
            106,
            29,
            23,
            180 * 16,
            180 * 16
        )

    def draw_happy_face(self, painter: QPainter) -> None:
        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawArc(
            50,
            91,
            19,
            17,
            0,
            -180 * 16
        )

        painter.drawArc(
            81,
            91,
            19,
            17,
            0,
            -180 * 16
        )

        painter.drawArc(
            62,
            105,
            27,
            25,
            180 * 16,
            180 * 16
        )

    def draw_worried_face(self, painter: QPainter) -> None:
        painter.drawEllipse(
            54,
            94,
            6,
            8
        )

        painter.drawEllipse(
            90,
            94,
            6,
            8
        )

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawArc(
            64,
            113,
            22,
            13,
            0,
            180 * 16
        )

    def draw_dramatic_face(self, painter: QPainter) -> None:
        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawLine(
            51,
            99,
            62,
            93
        )

        painter.drawLine(
            88,
            93,
            99,
            99
        )

        painter.setBrush(
            QColor("#18354A")
        )

        painter.drawEllipse(
            68,
            111,
            14,
            17
        )

    def draw_blush(self, painter: QPainter) -> None:
        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QColor(
                255,
                134,
                159,
                125
            )
        )

        painter.drawEllipse(
            42,
            109,
            15,
            8
        )

        painter.drawEllipse(
            94,
            109,
            15,
            8
        )
