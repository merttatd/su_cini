import random

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QRect,
    QPropertyAnimation,
    QTimer,
    Qt,
)
from PyQt6.QtGui import QCursor, QRegion
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)

from droplet_widget import DropletWidget


class PeekWindow(QWidget):
    def __init__(
        self,
        caught_callback=None
    ):
        super().__init__()

        self.caught_callback = caught_callback

        self.is_peeking = False
        self.hiding = False
        self.edge = None
        self.peek_geometry = None

        self.hidden_position = QPoint()
        self.visible_position = QPoint()

        self.animation = None
        self.auto_hide_timer = QTimer(self)
        self.auto_hide_timer.setSingleShot(True)

        self.auto_hide_timer.timeout.connect(
            self.hide_peek
        )

        self.configure_window()
        self.create_interface()

    def configure_window(self) -> None:
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_NoSystemBackground
        )

        self.setFixedSize(
            160,
            185
        )

    def create_interface(self) -> None:
        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.droplet = DropletWidget()
        self.droplet.set_mood("normal")

        layout.addWidget(
            self.droplet,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

    def show_peek(self) -> None:
        if self.is_peeking:
            return

        screen = QApplication.screenAt(QCursor.pos()) or QApplication.primaryScreen()

        if screen is None:
            return

        self.peek_geometry = screen.availableGeometry()
        self.edge = random.choice([edge for edge in ("right", "left", "top", "bottom")
                                   if edge != self.edge])
        self.hidden_position, self.visible_position = self.positions_for_edge(
            self.peek_geometry, self.edge)
        self.droplet.set_rotation(180 if self.edge == "top" else 0)

        self.move(
            self.hidden_position
        )

        self.is_peeking = True
        self.hiding = False
        self.update_edge_mask()
        self.show()
        self.raise_()

        self.animate_to(
            self.visible_position,
            duration=700,
            easing=QEasingCurve.Type.OutBack
        )

        self.auto_hide_timer.start(
            random.randint(
                4500,
                7500
            )
        )

    def positions_for_edge(self, geometry: QRect, edge: str) -> tuple[QPoint, QPoint]:
        def along_edge(start, length, size):
            low, high = start + 60, start + length - size - 60
            return random.randint(low, high) if high >= low else start + max(0, (length - size) // 2)

        if edge in ("left", "right"):
            y = along_edge(geometry.top(), geometry.height(), self.height())
            if edge == "left":
                return (QPoint(geometry.left() - self.width() - 10, y),
                        QPoint(geometry.left() - self.width() + 95, y))
            return (QPoint(geometry.right() + 11, y),
                    QPoint(geometry.right() + 1 - 95, y))
        x = along_edge(geometry.left(), geometry.width(), self.width())
        if edge == "top":
            return (QPoint(x, geometry.top() - self.height() - 10),
                    QPoint(x, geometry.top() - self.height() + 130))
        if edge == "bottom":
            return (QPoint(x, geometry.bottom() + 11),
                    QPoint(x, geometry.bottom() + 1 - 125))
        raise ValueError(f"Unknown peek edge: {edge}")

    def update_edge_mask(self) -> None:
        if self.peek_geometry is None:
            return
        visible = self.rect().intersected(self.peek_geometry.translated(-self.pos()))
        # An empty QRegion removes the mask; use a region outside the widget instead.
        self.setMask(QRegion(visible if not visible.isEmpty() else QRect(-2, -2, 1, 1)))

    def moveEvent(self, event) -> None:
        self.update_edge_mask()
        super().moveEvent(event)

    def hideEvent(self, event) -> None:
        self.auto_hide_timer.stop()
        if self.animation is not None:
            self.animation.stop()
        self.is_peeking = False
        self.hiding = False
        super().hideEvent(event)

    def hide_peek(self) -> None:
        if (
            not self.is_peeking
            or self.hiding
        ):
            return

        self.hiding = True
        self.auto_hide_timer.stop()

        self.animate_to(
            self.hidden_position,
            duration=450,
            easing=QEasingCurve.Type.InCubic,
            finished_callback=self.finish_hiding
        )

    def finish_hiding(self) -> None:
        self.hide()

        self.is_peeking = False
        self.hiding = False

    def animate_to(
        self,
        target: QPoint,
        duration: int,
        easing,
        finished_callback=None
    ) -> None:
        if self.animation is not None:
            self.animation.stop()

        self.animation = QPropertyAnimation(
            self,
            b"pos"
        )

        self.animation.setDuration(duration)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(target)
        self.animation.setEasingCurve(easing)

        if finished_callback:
            self.animation.finished.connect(
                finished_callback
            )

        self.animation.start()

    def enterEvent(self, event) -> None:
        if (
            self.is_peeking
            and not self.hiding
        ):
            if self.caught_callback:
                self.caught_callback()

            self.hide_peek()

        super().enterEvent(event)
