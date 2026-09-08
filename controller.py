import random

from datetime import datetime
from typing import Optional

from PyQt6.QtCore import (
    QSettings,
    QTimer,
    Qt,
)
from PyQt6.QtGui import (
    QAction,
    QActionGroup,
    QColor,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMenu,
    QSystemTrayIcon,
)

from activity_detector import ActivityDetector
from behavior_manager import BehaviorManager
from data_manager import DataManager
from goal_dialog import GoalDialog
from peek_window import PeekWindow
from reminder_window import ReminderWindow


APP_NAME = "Su Cini"
ORGANIZATION_NAME = "MertApps"


class WaterSpiritController:
    def __init__(
        self,
        application: QApplication
    ):
        self.application = application

        self.settings = QSettings(
            ORGANIZATION_NAME,
            APP_NAME
        )

        self.data_manager = DataManager()
        self.behavior_manager = BehaviorManager()
        self.activity_detector = ActivityDetector()

        self.last_drink = self.load_last_drink()

        self.snoozed_until: Optional[float] = None

        self.pending_fullscreen_reminder = False
        self.fullscreen_resume_scheduled = False
        self.was_fullscreen = False

        self.window = ReminderWindow(self)

        self.peek_window = PeekWindow(
            caught_callback=self.peek_caught
        )

        self.create_tray_icon()
        self.select_daily_goal()
        self.create_timers()
        self.schedule_next_peek()

        QTimer.singleShot(
            900,
            self.show_goal_message
        )

    def select_daily_goal(self) -> None:
        current_goal = (
            self.data_manager.get_daily_goal()
        )

        current_cup_size = (
            self.data_manager.get_cup_size()
        )

        dialog = GoalDialog(
            current_goal=current_goal,
            current_cup_size=current_cup_size
        )

        result = dialog.exec()

        if result:
            goal, cup_size = dialog.get_goal()

            self.data_manager.set_daily_goal(
                goal,
                cup_size
            )

    def create_timers(self) -> None:
        self.reminder_timer = QTimer(
            self.application
        )

        self.reminder_timer.setInterval(
            15_000
        )

        self.reminder_timer.timeout.connect(
            self.check_reminder
        )

        self.reminder_timer.start()

        self.activity_timer = QTimer(
            self.application
        )

        self.activity_timer.setInterval(
            3_000
        )

        self.activity_timer.timeout.connect(
            self.check_activity_state
        )

        self.activity_timer.start()

        self.peek_timer = QTimer(
            self.application
        )

        self.peek_timer.setSingleShot(True)

        self.peek_timer.timeout.connect(
            self.try_show_peek
        )

    def create_tray_icon(self) -> None:
        self.tray_icon = QSystemTrayIcon(
            self.create_icon(),
            self.application
        )

        self.tray_icon.setToolTip(
            "Su Cini — hidrasyon nöbetinde"
        )

        self.create_tray_menu()

        self.tray_icon.activated.connect(
            self.tray_icon_clicked
        )

        self.tray_icon.show()

    def create_icon(self) -> QIcon:
        pixmap = QPixmap(
            64,
            64
        )

        pixmap.fill(
            Qt.GlobalColor.transparent
        )

        painter = QPainter(pixmap)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        path = QPainterPath()

        path.moveTo(32, 4)

        path.cubicTo(
            25, 18,
            12, 30,
            12, 43
        )

        path.cubicTo(
            12, 56,
            20, 61,
            32, 61
        )

        path.cubicTo(
            44, 61,
            52, 56,
            52, 43
        )

        path.cubicTo(
            52, 30,
            39, 18,
            32, 4
        )

        painter.setBrush(
            QColor("#65C9FF")
        )

        painter.setPen(
            QPen(
                QColor("#258DCB"),
                3
            )
        )

        painter.drawPath(path)
        painter.end()

        return QIcon(pixmap)

    def create_tray_menu(self) -> None:
        old_menu = getattr(self, "tray_menu", None)
        menu = QMenu()
        self.tray_menu = menu

        show_action = QAction(
            "Su Cinini göster",
            menu
        )

        show_action.triggered.connect(
            self.show_manual_reminder
        )

        menu.addAction(show_action)

        drink_action = QAction(
            "Şimdi su içtim",
            menu
        )

        drink_action.triggered.connect(
            self.register_drink_from_tray
        )

        menu.addAction(drink_action)

        goal_action = QAction(
            "Günlük hedefi değiştir",
            menu
        )

        goal_action.triggered.connect(
            self.change_daily_goal
        )

        menu.addAction(goal_action)
        menu.addSeparator()

        interval_menu = menu.addMenu(
            "Hatırlatma aralığı"
        )

        current_interval = int(
            self.data_manager.get_setting(
                "reminder_interval",
                60
            )
        )

        interval_group = QActionGroup(menu)
        interval_group.setExclusive(True)
        for minutes in (
            30,
            45,
            60,
            90,
            120
        ):
            action = QAction(
                f"{minutes} dakika",
                interval_menu
            )

            action.setCheckable(True)
            interval_group.addAction(action)

            action.setChecked(
                minutes == current_interval
            )

            action.triggered.connect(
                lambda checked, value=minutes:
                self.set_interval(value)
            )

            interval_menu.addAction(action)

        menu.addSeparator()

        stats_action = QAction(
            "Bugünkü ilerlemeyi göster",
            menu
        )

        stats_action.triggered.connect(
            self.show_today_progress
        )

        menu.addAction(stats_action)

        peek_action = QAction(
            "Su Cini nereye saklandı?",
            menu
        )

        peek_action.triggered.connect(
            self.show_manual_peek
        )

        menu.addAction(peek_action)
        menu.addSeparator()

        exit_action = QAction(
            "Çıkış",
            menu
        )

        exit_action.triggered.connect(
            self.application.quit
        )

        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        if old_menu is not None:
            old_menu.deleteLater()

    def load_last_drink(self) -> datetime:
        saved_value = self.data_manager.data["behavior"].get("last_drink_time") or self.settings.value(
            "last_drink"
        )

        if saved_value:
            try:
                saved = datetime.fromisoformat(str(saved_value))
                saved = datetime.fromtimestamp(saved.timestamp())
                return min(saved, datetime.now())

            except (ValueError, TypeError, OverflowError, OSError):
                pass

        return datetime.now()

    def show_goal_message(self) -> None:
        goal = (
            self.data_manager.get_daily_goal()
        )

        message = (
            self.behavior_manager
            .goal_selected_message(goal)
        )

        self.window.show_reminder(
            "happy",
            message
        )

    def change_daily_goal(self) -> None:
        dialog = GoalDialog(
            current_goal=(
                self.data_manager.get_daily_goal()
            ),

            current_cup_size=(
                self.data_manager.get_cup_size()
            )
        )

        if not dialog.exec():
            return

        goal, cup_size = dialog.get_goal()

        self.data_manager.set_daily_goal(
            goal,
            cup_size
        )

        message = (
            self.behavior_manager
            .goal_selected_message(goal)
        )

        self.window.show_reminder(
            "happy",
            message
        )

        self.create_tray_menu()

    def register_drink(self) -> dict:
        drink_result = self.data_manager.register_drink()
        self.last_drink = datetime.now()
        self.snoozed_until = None
        self.pending_fullscreen_reminder = False

        self.settings.setValue(
            "last_drink",
            self.last_drink.isoformat()
        )

        message = (
            self.behavior_manager
            .drink_message(drink_result)
        )

        goal_complete = (
            drink_result["drink_count"]
            >= drink_result["goal"]
        )

        return {
            "message": message,
            "mood": (
                "happy"
                if not drink_result["rapid_drink"]
                else "worried"
            ),
            "drink_count":
                drink_result["drink_count"],
            "goal":
                drink_result["goal"],
            "total_ml":
                drink_result["total_ml"],
            "goal_complete":
                goal_complete,
        }

    def register_drink_from_tray(self) -> None:
        result = self.register_drink()

        self.window.show_reminder(
            result["mood"],
            result["message"]
        )

        self.window.hide_after(2800)

    def snooze(self) -> dict:
        snooze_result = self.data_manager.register_snooze()
        self.pending_fullscreen_reminder = False
        self.snoozed_until = (
            datetime.now().timestamp()
            + (5 * 60)
        )

        message = (
            self.behavior_manager
            .snooze_message(snooze_result)
        )

        consecutive = snooze_result[
            "consecutive_snoozes"
        ]

        mood = (
            "dramatic"
            if consecutive >= 4
            else "worried"
        )

        return {
            "message": message,
            "mood": mood,
        }

    def check_reminder(self) -> None:
        current_time = datetime.now()
        self.window.update_progress(*self.get_progress())
        if (self.window.isVisible() or self.fullscreen_resume_scheduled
                or QApplication.activeModalWidget() is not None):
            return

        if (
            self.snoozed_until is not None
            and current_time.timestamp()
            < self.snoozed_until
        ):
            return

        interval_minutes = int(
            self.data_manager.get_setting(
                "reminder_interval",
                60
            )
        )

        elapsed_minutes = (
            current_time - self.last_drink
        ).total_seconds() / 60

        snooze_due = self.snoozed_until is not None
        if elapsed_minutes < interval_minutes and not snooze_due:
            return

        if self.activity_detector.is_fullscreen_active():
            self.pending_fullscreen_reminder = True
            return

        self.pending_fullscreen_reminder = False

        interval_ratio = (
            elapsed_minutes
            / max(interval_minutes, 1)
        )

        if interval_ratio >= 2:
            mood = "dramatic"

        elif interval_ratio >= 1.35:
            mood = "worried"

        else:
            mood = "normal"

        message = (
            self.behavior_manager
            .reminder_message(mood)
        )

        self.window.show_reminder(
            mood,
            message
        )

        self.snoozed_until = (
            current_time.timestamp()
            + (10 * 60)
        )

    def check_activity_state(self) -> None:
        fullscreen_now = (
            self.activity_detector
            .is_fullscreen_active()
        )

        if (
            not fullscreen_now
            and self.pending_fullscreen_reminder
            and not self.fullscreen_resume_scheduled
        ):
            self.fullscreen_resume_scheduled = True

            QTimer.singleShot(
                25_000,
                self.show_deferred_reminder
            )

        self.was_fullscreen = fullscreen_now

    def show_deferred_reminder(self) -> None:
        self.fullscreen_resume_scheduled = False

        if (
            self.activity_detector
            .is_fullscreen_active()
        ):
            return

        if not self.pending_fullscreen_reminder:
            return

        now = datetime.now().timestamp()
        interval = self.data_manager.get_setting("reminder_interval", 60) * 60
        if self.snoozed_until is not None and now < self.snoozed_until:
            self.pending_fullscreen_reminder = False
            return
        if self.snoozed_until is None and now - self.last_drink.timestamp() < interval:
            self.pending_fullscreen_reminder = False
            return
        if self.window.isVisible():
            self.pending_fullscreen_reminder = False
            return

        self.pending_fullscreen_reminder = False

        message = (
            self.behavior_manager
            .fullscreen_return_message()
        )

        self.window.show_reminder(
            "normal",
            message
        )

        self.snoozed_until = (
            datetime.now().timestamp()
            + (10 * 60)
        )

    def show_manual_reminder(self) -> None:
        message = (
            self.behavior_manager
            .reminder_message("normal")
        )

        self.window.show_reminder(
            "normal",
            message
        )

    def show_today_progress(self) -> None:
        stats = (
            self.data_manager.get_today_stats()
        )

        current = stats["drink_count"]
        goal = stats["goal"]
        total_ml = stats["total_ml"]

        if current >= goal:
            message = (
                f"Bugünkü hedef tamamlandı: "
                f"{current}/{goal} bardak ve "
                f"{total_ml} ml."
            )

            mood = "happy"

        elif current == 0:
            message = (
                f"Bugünkü hedef {goal} bardak. "
                "Henüz ilk yudumu bekliyorum."
            )

            mood = "worried"

        else:
            message = (
                f"Bugün {current}/{goal} bardaktayız. "
                f"Toplam {total_ml} ml."
            )

            mood = "normal"

        self.window.show_reminder(
            mood,
            message
        )

    def get_progress(
        self
    ) -> tuple[int, int, int]:
        stats = (
            self.data_manager.get_today_stats()
        )

        return (
            stats["drink_count"],
            stats["goal"],
            stats["total_ml"]
        )

    def set_interval(
        self,
        minutes: int
    ) -> None:
        self.data_manager.set_setting(
            "reminder_interval",
            minutes
        )

        self.create_tray_menu()

        self.window.show_reminder(
            "happy",
            (
                f"Tamamdır. Bundan sonra "
                f"{minutes} dakikada bir geleceğim."
            )
        )

        self.window.hide_after(2600)

    def schedule_next_peek(self) -> None:
        
        delay_minutes = random.randint(
            15,
            30
        )

        self.peek_timer.start(
            delay_minutes * 60 * 1000
        )

    def try_show_peek(self) -> None:
        should_skip = (
            QApplication.activeModalWidget() is not None
            or
            self.activity_detector
            .is_fullscreen_active()
            or self.window.isVisible()
            or self.window.is_being_dragged()
            or self.peek_window.is_peeking
        )

        if should_skip:
            self.peek_timer.start(
                5 * 60 * 1000
            )
            return

        self.peek_window.show_peek()
        self.schedule_next_peek()

    def show_manual_peek(self) -> None:
        if (
            self.activity_detector
            .is_fullscreen_active()
        ):
            return

        if self.window.isVisible():
            return

        self.peek_window.show_peek()

    def peek_caught(self) -> None:
        # Normalde sadece kaçar.
        # Yaklaşık üç yakalanmadan birinde konuşur.
        if random.randint(1, 3) != 1:
            return

        message = (
            self.behavior_manager
            .peek_caught_message()
        )

        def show_caught_message():
            if self.window.isVisible() or self.activity_detector.is_fullscreen_active():
                return
            self.window.show_reminder("worried", message)
            self.window.hide_after(1900)

        QTimer.singleShot(500, show_caught_message)

    def tray_icon_clicked(
        self,
        reason
    ) -> None:
        if (
            reason
            == QSystemTrayIcon.ActivationReason.Trigger
        ):
            self.show_manual_reminder()
