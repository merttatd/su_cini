from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QTimer,
    Qt,
)
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from droplet_widget import DropletWidget


class ReminderWindow(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.drag_position = None
        self.slide_animation = None
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.reset_and_hide)

        self.configure_window()
        self.create_interface()
        self.create_animations()

    def configure_window(self) -> None:
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_NoSystemBackground
        )

        self.setFixedSize(
            360,
            365
        )

    def create_interface(self) -> None:
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            10,
            5,
            10,
            10
        )

        main_layout.setSpacing(0)

        self.message_bubble = QLabel(
            "Minik bir su molası versek mi?"
        )

        self.message_bubble.setWordWrap(True)

        self.message_bubble.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.message_bubble.setFixedWidth(
            305
        )

        self.message_bubble.setMinimumHeight(
            75
        )

        self.message_bubble.setMaximumHeight(
            110
        )

        self.message_bubble.setStyleSheet(
            """
            QLabel {
                background-color: rgba(255, 255, 255, 245);
                color: #18354A;

                border: 2px solid rgba(78, 174, 225, 230);
                border-radius: 20px;

                padding: 12px 18px;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
            }
            """
        )

        main_layout.addWidget(
            self.message_bubble,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.bubble_tail = QLabel("▼")

        self.bubble_tail.setFixedHeight(18)

        self.bubble_tail.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.bubble_tail.setStyleSheet(
            """
            QLabel {
                color: rgba(78, 174, 225, 230);
                background: transparent;
                font-size: 22px;
                font-weight: bold;
            }
            """
        )

        main_layout.addWidget(
            self.bubble_tail,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.droplet = DropletWidget()

        main_layout.addWidget(
            self.droplet,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.progress_label = QLabel(
            "Bugün: 0 / 8 bardak"
        )

        self.progress_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.progress_label.setStyleSheet(
            """
            QLabel {
                color: #176C9F;
                background-color: rgba(235, 248, 255, 220);
                border: 1px solid rgba(105, 199, 248, 180);
                border-radius: 10px;
                padding: 5px 12px;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 700;
            }
            """
        )

        main_layout.addWidget(
            self.progress_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addSpacing(7)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.drink_button = QPushButton(
            "💧 Su içtim"
        )

        self.snooze_button = QPushButton(
            "5 dk ertele"
        )

        self.drink_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.snooze_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.drink_button.clicked.connect(
            self.drink_water
        )

        self.snooze_button.clicked.connect(
            self.snooze_reminder
        )

        button_layout.addStretch()
        button_layout.addWidget(
            self.drink_button
        )

        button_layout.addWidget(
            self.snooze_button
        )

        button_layout.addStretch()

        main_layout.addLayout(
            button_layout
        )

        self.setStyleSheet(
            """
            QPushButton {
                min-height: 38px;

                padding-left: 17px;
                padding-right: 17px;

                background-color: rgba(235, 248, 255, 235);
                color: #176C9F;

                border: 1px solid rgba(105, 199, 248, 220);
                border-radius: 14px;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: rgba(207, 239, 255, 245);
                border: 1px solid #48B8EE;
            }

            QPushButton:pressed {
                background-color: rgba(181, 228, 251, 250);
                padding-top: 2px;
            }

            QPushButton:disabled {
                background-color: rgba(230, 238, 242, 190);
                color: rgba(92, 116, 128, 170);
                border-color: rgba(150, 175, 188, 150);
            }
            """
        )

    def create_animations(self) -> None:
        self.fade_animation = QPropertyAnimation(
            self,
            b"windowOpacity"
        )

        self.fade_animation.setDuration(400)

        self.fade_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

    def show_reminder(
        self,
        mood: str,
        message: str,
        preserve_position: bool = False
    ) -> None:
        self.hide_timer.stop()
        self.drink_button.setEnabled(True)
        self.snooze_button.setEnabled(True)
        if self.slide_animation is not None:
            self.slide_animation.stop()
        self.droplet.set_mood(mood)
        self.message_bubble.setText(message)

        self.update_progress(
            *self.controller.get_progress()
        )
        self.setFixedHeight(max(365, self.layout().totalHeightForWidth(self.width())))

        if self.isVisible():
            return

        screen = QApplication.primaryScreen()

        if screen is None:
            return

        screen_geometry = (
            screen.availableGeometry()
        )

        if (
            preserve_position
            and self.isVisible()
        ):
            final_position = self.pos()

        else:
            final_position = QPoint(
                screen_geometry.right()
                - self.width()
                - 20,

                screen_geometry.bottom()
                - self.height()
                - 15
            )

        starting_position = QPoint(
            final_position.x(),
            final_position.y() + 30
        )

        self.move(starting_position)
        self.setWindowOpacity(0.0)

        self.show()
        self.raise_()

        self.fade_animation.stop()

        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

        self.slide_animation = QPropertyAnimation(
            self,
            b"pos"
        )

        self.slide_animation.setDuration(450)
        self.slide_animation.setStartValue(
            starting_position
        )

        self.slide_animation.setEndValue(
            final_position
        )

        self.slide_animation.setEasingCurve(
            QEasingCurve.Type.OutBack
        )

        self.slide_animation.start()

    def update_progress(
        self,
        current: int,
        goal: int,
        total_ml: int
    ) -> None:
        self.progress_label.setText(
            f"Bugün: {current} / {goal} bardak"
            f"  •  {total_ml} ml"
        )

    def drink_water(self) -> None:
        result = self.controller.register_drink()

        self.droplet.set_mood(
            result["mood"]
        )

        self.message_bubble.setText(
            result["message"]
        )

        self.update_progress(
            result["drink_count"],
            result["goal"],
            result["total_ml"]
        )

        self.disable_buttons()

        self.hide_after(2800)

    def snooze_reminder(self) -> None:
        result = self.controller.snooze()

        self.droplet.set_mood(
            result["mood"]
        )

        self.message_bubble.setText(
            result["message"]
        )

        self.disable_buttons()

        self.hide_after(2400)

    def hide_after(self, milliseconds: int) -> None:
        self.hide_timer.start(milliseconds)

    def disable_buttons(self) -> None:
        self.drink_button.setEnabled(False)
        self.snooze_button.setEnabled(False)

    def reset_and_hide(self) -> None:
        self.hide_timer.stop()
        self.fade_animation.stop()
        if self.slide_animation is not None:
            self.slide_animation.stop()
        self.drag_position = None
        self.drink_button.setEnabled(True)
        self.snooze_button.setEnabled(True)

        self.droplet.set_mood("normal")

        self.hide()

    def mousePressEvent(self, event) -> None:
        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):
            if (
                self.slide_animation is not None
                and self.slide_animation.state()
                == QPropertyAnimation.State.Running
            ):
                self.slide_animation.stop()

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if (
            self.drag_position is not None
            and event.buttons()
            & Qt.MouseButton.LeftButton
        ):
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self.drag_position = None
        event.accept()

    def is_being_dragged(self) -> bool:
        return self.drag_position is not None
