from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from droplet_widget import DropletWidget


class GoalCycleDialog(QDialog):
    """Su Cini temasında hedef döngüsü seçim penceresi."""

    REPEAT_GOAL = 1
    NEW_GOAL = 2

    def __init__(self, current_goal: int, current_cup_size: int, parent=None):
        super().__init__(parent)
        self.choice = self.REPEAT_GOAL
        self.current_goal = current_goal
        self.current_cup_size = current_cup_size
        self.configure_window()
        self.create_interface()

    def configure_window(self) -> None:
        self.setWindowTitle("Su Cini — Hedef tamamlandı!")
        self.setFixedSize(500, 430)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def create_interface(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)

        card = QWidget()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 22, 30, 28)
        layout.setSpacing(10)

        self.droplet = DropletWidget()
        self.droplet.set_mood("happy")
        layout.addWidget(self.droplet, 0, Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("Hedef tamamlandı! ♥")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        message = QLabel(
            f"{self.current_goal} bardaklık hedefi tamamladın!\n"
            "Su Cini yeni tur için ne yapmak istediğini merak ediyor."
        )
        message.setObjectName("message")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setWordWrap(True)
        layout.addWidget(message)

        info = QLabel(
            f"Mevcut hedef  •  {self.current_goal} bardak  •  "
            f"{self.current_cup_size} ml"
        )
        info.setObjectName("info")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        buttons = QHBoxLayout()
        buttons.setSpacing(12)

        repeat_button = QPushButton("↻  Aynı hedefi tekrarla")
        repeat_button.setObjectName("repeatButton")
        repeat_button.setCursor(Qt.CursorShape.PointingHandCursor)
        repeat_button.setDefault(True)
        repeat_button.clicked.connect(self.repeat_goal)

        new_goal_button = QPushButton("✦  Yeni bir hedef seç")
        new_goal_button.setObjectName("newGoalButton")
        new_goal_button.setCursor(Qt.CursorShape.PointingHandCursor)
        new_goal_button.clicked.connect(self.choose_new_goal)

        buttons.addWidget(repeat_button)
        buttons.addWidget(new_goal_button)
        layout.addSpacing(6)
        layout.addLayout(buttons)

        outer.addWidget(card)

        self.setStyleSheet("""
            QWidget#card {
                background-color: rgba(248, 253, 255, 252);
                border: 2px solid #63C3F4;
                border-radius: 28px;
            }
            QLabel {
                background: transparent;
                border: none;
                font-family: "Segoe UI";
            }
            QLabel#title {
                color: #1872A6;
                font-size: 22px;
                font-weight: 800;
            }
            QLabel#message {
                color: #28546C;
                font-size: 14px;
                font-weight: 600;
            }
            QLabel#info {
                color: #176C9F;
                background-color: rgba(225, 245, 255, 190);
                border: 1px solid rgba(105, 199, 248, 150);
                border-radius: 11px;
                padding: 9px;
                font-size: 12px;
                font-weight: 700;
            }
            QPushButton {
                min-height: 48px;
                border-radius: 15px;
                padding: 0 14px;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton#repeatButton {
                background-color: #45B5EB;
                color: white;
                border: none;
            }
            QPushButton#repeatButton:hover {
                background-color: #299FD9;
            }
            QPushButton#repeatButton:pressed {
                background-color: #208FC3;
            }
            QPushButton#newGoalButton {
                background-color: #E9F7FF;
                color: #1872A6;
                border: 1px solid #79CAF3;
            }
            QPushButton#newGoalButton:hover {
                background-color: #D4F0FF;
                border-color: #4EB7EA;
            }
            QPushButton#newGoalButton:pressed {
                background-color: #BFE9FC;
            }
        """)

    def repeat_goal(self) -> None:
        self.choice = self.REPEAT_GOAL
        self.accept()

    def choose_new_goal(self) -> None:
        self.choice = self.NEW_GOAL
        self.accept()
