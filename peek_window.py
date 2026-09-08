import random

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QTimer,
    Qt,
)
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

        screen = QApplication.primaryScreen()

        if screen is None:
            return

        geometry = screen.availableGeometry()

        minimum_y = geometry.top() + 80

        maximum_y = (
            geometry.bottom()
            - self.height()
            - 100
        )

        if maximum_y <= minimum_y:
            peek_y = max(geometry.top(), geometry.center().y() - self.height() // 2)
        else:
            peek_y = random.randint(
                minimum_y,
                maximum_y
            )

        hidden_x = (
            geometry.right() + 10
        )

        visible_x = (
            geometry.right()
            - 58
        )

        self.hidden_position = QPoint(
            hidden_x,
            peek_y
        )

        self.visible_position = QPoint(
            visible_x,
            peek_y
        )

        self.move(
            self.hidden_position
        )

        self.show()
        self.raise_()

        self.is_peeking = True
        self.hiding = False

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
