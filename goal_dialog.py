from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class NumberStepper(QWidget):
    value_changed = pyqtSignal(int)

    def __init__(
        self,
        value: int,
        minimum: int,
        maximum: int,
        step: int,
        suffix: str = "",
        parent=None
    ):
        super().__init__(parent)

        self._value = max(minimum, min(maximum, value))
        self.minimum = minimum
        self.maximum = maximum
        self.step = step
        self.suffix = suffix

        self.setObjectName("numberStepper")

        self.create_interface()
        self.update_value_label()

    def create_interface(self) -> None:
        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.minus_button = QPushButton("−")
        self.minus_button.setObjectName("stepButton")
        self.minus_button.setFixedSize(42, 42)
        self.minus_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.value_label = QLabel()
        self.value_label.setObjectName("stepValue")
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value_label.setMinimumWidth(110)
        self.value_label.setFixedHeight(42)

        self.plus_button = QPushButton("+")
        self.plus_button.setObjectName("stepButton")
        self.plus_button.setFixedSize(42, 42)
        self.plus_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.minus_button.clicked.connect(
            self.decrease_value
        )

        self.plus_button.clicked.connect(
            self.increase_value
        )

        layout.addWidget(self.minus_button)
        layout.addWidget(self.value_label)
        layout.addWidget(self.plus_button)

    def decrease_value(self) -> None:
        self.set_value(
            self._value - self.step
        )

    def increase_value(self) -> None:
        self.set_value(
            self._value + self.step
        )

    def set_value(self, value: int) -> None:
        new_value = max(
            self.minimum,
            min(self.maximum, value)
        )

        if new_value == self._value:
            return

        self._value = new_value

        self.update_value_label()
        self.value_changed.emit(self._value)

    def value(self) -> int:
        return self._value

    def update_value_label(self) -> None:
        self.value_label.setText(
            f"{self._value}{self.suffix}"
        )

        self.minus_button.setEnabled(
            self._value > self.minimum
        )

        self.plus_button.setEnabled(
            self._value < self.maximum
        )


class GoalDialog(QDialog):
    def __init__(
        self,
        current_goal: int = 8,
        current_cup_size: int = 250,
        parent=None
    ):
        super().__init__(parent)

        self.selected_goal = current_goal
        self.selected_cup_size = current_cup_size

        self.goal_buttons: dict[int, QPushButton] = {}

        self.configure_window()

        self.create_interface(
            current_goal,
            current_cup_size
        )

    def configure_window(self) -> None:
        self.setWindowTitle(
            "Bugünkü Su Hedefi"
        )

        # Üst başlık ve kontroller için alan artırıldı.
        self.setFixedSize(
            460,
            500
        )

        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def create_interface(
        self,
        current_goal: int,
        current_cup_size: int
    ) -> None:
        outer_layout = QVBoxLayout(self)

        outer_layout.setContentsMargins(
            14,
            14,
            14,
            14
        )

        card = QWidget()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)

        card_layout.setContentsMargins(
            28,
            20,
            28,
            24
        )

        card_layout.setSpacing(13)

        # Üst bölüm
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")

        header_layout = QVBoxLayout(
            header_widget
        )

        header_layout.setContentsMargins(
            0,
            0,
            0,
            6
        )

        header_layout.setSpacing(6)

        character = QLabel("💧")

        character.setFixedHeight(52)

        character.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        character.setStyleSheet(
            """
            QLabel {
                color: #47B7EE;
                font-size: 43px;
                background: transparent;
                border: none;
            }
            """
        )

        title = QLabel(
            "Bugün kaç bardaklık\n"
            "bir maceraya çıkıyoruz?"
        )

        title.setWordWrap(True)

        title.setMinimumHeight(58)

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            QLabel {
                color: #18354A;
                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
                background: transparent;
                border: none;
            }
            """
        )

        header_layout.addWidget(character)
        header_layout.addWidget(title)

        card_layout.addWidget(header_widget)

        # Hazır hedef seçenekleri
        options_layout = QHBoxLayout()

        options_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        options_layout.setSpacing(8)

        self.goal_group = QButtonGroup(self)
        self.goal_group.setExclusive(True)

        for goal in (6, 8, 10, 12):
            button = QPushButton(str(goal))

            button.setCheckable(True)
            button.setProperty(
                "goalButton",
                True
            )

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            button.clicked.connect(
                lambda checked, value=goal:
                self.select_goal(value)
            )

            if goal == current_goal:
                button.setChecked(True)

            self.goal_group.addButton(button)

            self.goal_buttons[goal] = button

            options_layout.addWidget(button)

        card_layout.addLayout(options_layout)

        # Özel hedef
        custom_row = QWidget()
        custom_row.setObjectName("settingRow")

        custom_layout = QHBoxLayout(
            custom_row
        )

        custom_layout.setContentsMargins(
            14,
            8,
            8,
            8
        )

        custom_layout.setSpacing(12)

        custom_label = QLabel(
            "Özel hedef"
        )

        custom_label.setObjectName(
            "settingLabel"
        )

        self.custom_goal = NumberStepper(
            value=current_goal,
            minimum=1,
            maximum=30,
            step=1,
            suffix=" bardak"
        )

        self.custom_goal.value_changed.connect(
            self.select_custom_goal
        )

        custom_layout.addWidget(custom_label)
        custom_layout.addStretch()
        custom_layout.addWidget(self.custom_goal)

        card_layout.addWidget(custom_row)

        # Bardak miktarı
        cup_row = QWidget()
        cup_row.setObjectName("settingRow")

        cup_layout = QHBoxLayout(
            cup_row
        )

        cup_layout.setContentsMargins(
            14,
            8,
            8,
            8
        )

        cup_layout.setSpacing(12)

        cup_label = QLabel(
            "Bir bardak"
        )

        cup_label.setObjectName(
            "settingLabel"
        )

        self.cup_size = NumberStepper(
            value=current_cup_size,
            minimum=50,
            maximum=1000,
            step=50,
            suffix=" ml"
        )

        self.cup_size.value_changed.connect(
            self.update_total_text
        )

        cup_layout.addWidget(cup_label)
        cup_layout.addStretch()
        cup_layout.addWidget(self.cup_size)

        card_layout.addWidget(cup_row)

        self.total_label = QLabel()

        self.total_label.setObjectName(
            "totalLabel"
        )

        self.total_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        card_layout.addWidget(
            self.total_label
        )

        start_button = QPushButton(
            "Bugünkü görevi başlat"
        )

        start_button.setObjectName(
            "startButton"
        )

        start_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        start_button.clicked.connect(
            self.confirm_goal
        )

        card_layout.addWidget(
            start_button
        )

        outer_layout.addWidget(card)

        self.apply_styles()
        self.update_total_text()

    def apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QWidget#card {
                background-color: rgba(248, 253, 255, 250);
                border: 2px solid #63C3F4;
                border-radius: 28px;
            }

            QWidget#headerWidget {
                background: transparent;
                border: none;
            }

            QLabel {
                color: #28546C;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton[goalButton="true"] {
                min-width: 68px;
                min-height: 48px;

                background-color: rgba(233, 247, 255, 240);
                color: #1872A6;

                border: 1px solid #79CAF3;
                border-radius: 14px;

                font-family: "Segoe UI";
                font-size: 15px;
                font-weight: 700;
            }

            QPushButton[goalButton="true"]:hover {
                background-color: #D4F0FF;
                border: 1px solid #4EB7EA;
            }

            QPushButton[goalButton="true"]:checked {
                background-color: #58BFF2;
                color: white;

                border: 2px solid #258EC7;
            }

            QPushButton[goalButton="true"]:pressed {
                background-color: #3CA9DE;
            }

            QWidget#settingRow {
                background-color: rgba(235, 248, 255, 210);

                border: 1px solid rgba(105, 199, 248, 190);
                border-radius: 15px;
            }

            QLabel#settingLabel {
                color: #28546C;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }

            QWidget#numberStepper {
                background: transparent;
                border: none;
            }

            QLabel#stepValue {
                background-color: white;
                color: #24536D;

                border-top: 1px solid #75C6EE;
                border-bottom: 1px solid #75C6EE;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#stepButton {
                background-color: #65C4F1;
                color: white;

                border: 1px solid #3AA6DB;

                font-family: "Segoe UI";
                font-size: 21px;
                font-weight: 700;
            }

            QPushButton#stepButton:first-child {
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
            }

            QPushButton#stepButton:last-child {
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }

            QPushButton#stepButton:hover {
                background-color: #46B4E8;
            }

            QPushButton#stepButton:pressed {
                background-color: #269ACF;
            }

            QPushButton#stepButton:disabled {
                background-color: #C9E5F2;
                color: rgba(255, 255, 255, 170);
                border-color: #B1D7E8;
            }

            QLabel#totalLabel {
                color: #176C9F;

                background-color: rgba(225, 245, 255, 180);

                border: 1px solid rgba(105, 199, 248, 130);
                border-radius: 11px;

                padding: 8px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#startButton {
                min-height: 46px;

                background-color: #45B5EB;
                color: white;

                border: none;
                border-radius: 15px;

                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton#startButton:hover {
                background-color: #299FD9;
            }

            QPushButton#startButton:pressed {
                background-color: #238FC3;
                padding-top: 2px;
            }
            """
        )

    def select_goal(
        self,
        goal: int
    ) -> None:
        self.selected_goal = goal

        self.custom_goal.set_value(goal)

        self.update_total_text()

    def select_custom_goal(
        self,
        goal: int
    ) -> None:
        self.selected_goal = goal

        if goal in self.goal_buttons:
            self.goal_buttons[
                goal
            ].setChecked(True)

        else:
            checked_button = (
                self.goal_group.checkedButton()
            )

            if checked_button:
                self.goal_group.setExclusive(False)

                checked_button.setChecked(False)

                self.goal_group.setExclusive(True)

        self.update_total_text()

    def update_total_text(self) -> None:
        goal = self.custom_goal.value()
        cup_size = self.cup_size.value()

        self.selected_goal = goal
        self.selected_cup_size = cup_size

        total_ml = goal * cup_size

        if total_ml >= 1000:
            total_text = (
                f"{total_ml / 1000:g} litre"
            )
        else:
            total_text = (
                f"{total_ml} ml"
            )

        self.total_label.setText(
            f"Bugünkü toplam hedef: {total_text}"
        )

    def confirm_goal(self) -> None:
        self.selected_goal = (
            self.custom_goal.value()
        )

        self.selected_cup_size = (
            self.cup_size.value()
        )

        self.accept()

    def get_goal(self) -> tuple[int, int]:
        return (
            self.selected_goal,
            self.selected_cup_size
        )
