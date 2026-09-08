import json
import os
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from data_manager import DataManager
from behavior_manager import BehaviorManager
from messages import MESSAGES


class DataTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "data.json"
        self.manager = DataManager(self.path)

    def yesterday(self):
        self.manager.data["last_date"] = (date.today() - timedelta(days=1)).isoformat()

    def test_midnight_stats(self):
        self.manager.register_drink()
        self.yesterday()
        self.assertEqual(self.manager.get_today_stats()["drink_count"], 0)
        self.assertEqual(len(self.manager.data["history"]), 1)

    def test_midnight_drink(self):
        self.manager.register_drink()
        self.yesterday()
        result = self.manager.register_drink()
        self.assertEqual(result["drink_count"], 1)
        self.assertFalse(result["rapid_drink"])

    def test_midnight_snooze(self):
        self.manager.register_snooze()
        self.yesterday()
        self.assertEqual(self.manager.register_snooze()["consecutive_snoozes"], 1)

    def test_invalid_values_repaired(self):
        self.path.write_text(json.dumps({"settings": {"daily_goal": "bad", "cup_size_ml": -1},
                                         "today": {"drink_count": None}}))
        manager = DataManager(self.path)
        self.assertEqual(manager.register_drink()["total_ml"], 250)
        self.assertEqual(manager.get_daily_goal(), 8)

    def test_corrupt_file_preserved(self):
        self.path.write_bytes(b"\xffbroken")
        manager = DataManager(self.path)
        self.assertEqual(manager.get_daily_goal(), 8)
        self.assertEqual(self.path.with_suffix(".json.corrupt").read_bytes(), b"\xffbroken")

    def test_failed_save_preserves_file_and_memory(self):
        self.manager.register_drink()
        before = self.path.read_bytes()
        with patch("data_manager.os.replace", side_effect=PermissionError("locked")):
            with self.assertRaises(PermissionError):
                self.manager.register_drink()
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.manager.get_today_stats()["drink_count"], 1)
        self.assertEqual(list(self.path.parent.glob("*.tmp")), [])

    def test_invalid_timestamp(self):
        for value in (123, "invalid", "2026-01-01T10:00:00+03:00"):
            self.manager.data["behavior"]["last_drink_time"] = value
            self.manager.register_drink()

    def test_cup_change_preserves_previous_volume(self):
        self.manager.register_drink()
        self.manager.set_daily_goal(10, 300)
        self.assertEqual(self.manager.register_drink()["total_ml"], 550)

    def test_invalid_settings_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.set_setting("reminder_interval", 0)
        with self.assertRaises(ValueError):
            self.manager.set_daily_goal(0, 250)

    def test_odd_goal_halfway(self):
        result = dict(drink_count=4, drink_streak=1, goal=7, rapid_drink=False)
        self.assertIn(BehaviorManager().drink_message(result), MESSAGES["goal_half"])


from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from controller import WaterSpiritController
from reminder_window import ReminderWindow
from goal_dialog import GoalDialog, NumberStepper
from activity_detector import ActivityDetector


class InterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.controller = WaterSpiritController.__new__(WaterSpiritController)
        c = self.controller
        c.application = self.app
        c.data_manager = DataManager(Path(self.folder.name) / "data.json")
        c.behavior_manager = BehaviorManager()
        c.activity_detector = Mock()
        c.activity_detector.is_fullscreen_active.return_value = False
        c.settings = Mock()
        c.last_drink = datetime.now() - timedelta(hours=2)
        c.snoozed_until = None
        c.pending_fullscreen_reminder = False
        c.fullscreen_resume_scheduled = False
        c.was_fullscreen = False
        c.window = ReminderWindow(c)
        self.addCleanup(c.window.close)

    def test_new_message_cancels_old_hide(self):
        w = self.controller.window
        w.show_reminder("normal", "first")
        w.disable_buttons()
        w.hide_after(20)
        w.show_reminder("happy", "second")
        QTest.qWait(50)
        self.assertTrue(w.isVisible())
        self.assertTrue(w.drink_button.isEnabled())
        self.assertEqual(w.message_bubble.text(), "second")

    def test_hidden_animation_stops(self):
        w = self.controller.window
        w.show_reminder("normal", "test")
        self.assertEqual(w.droplet.bob_animation.state(), QPropertyAnimation.State.Running)
        w.reset_and_hide()
        self.assertEqual(w.droplet.bob_animation.state(), QPropertyAnimation.State.Stopped)

    def test_drink_cancels_deferred(self):
        c = self.controller
        c.pending_fullscreen_reminder = True
        c.register_drink()
        c.show_deferred_reminder()
        self.assertFalse(c.window.isVisible())

    def test_expired_manual_snooze_works_before_interval(self):
        c = self.controller
        c.last_drink = datetime.now()
        c.snoozed_until = datetime.now().timestamp() - 1
        c.check_reminder()
        self.assertTrue(c.window.isVisible())

    def test_fullscreen_wait_is_not_bypassed(self):
        c = self.controller
        c.fullscreen_resume_scheduled = True
        c.check_reminder()
        self.assertFalse(c.window.isVisible())

    def test_fullscreen_defers_and_returns(self):
        c = self.controller
        c.activity_detector.is_fullscreen_active.return_value = True
        c.check_reminder()
        self.assertTrue(c.pending_fullscreen_reminder)
        self.assertFalse(c.window.isVisible())
        c.activity_detector.is_fullscreen_active.return_value = False
        c.show_deferred_reminder()
        self.assertTrue(c.window.isVisible())
        self.assertFalse(c.pending_fullscreen_reminder)

    def test_stepper_and_goal_sync(self):
        stepper = NumberStepper(99, 1, 30, 1)
        self.assertEqual(stepper.value(), 30)
        dialog = GoalDialog()
        dialog.select_goal(10)
        dialog.custom_goal.increase_value()
        self.assertEqual(dialog.get_goal(), (11, 250))
        self.assertIsNone(dialog.goal_group.checkedButton())
        dialog.close()

    def test_windows_signatures(self):
        detector = ActivityDetector()
        if not detector.is_windows:
            self.skipTest("Windows only")
        import ctypes
        self.assertEqual(ctypes.sizeof(detector.user32.MonitorFromWindow.restype), ctypes.sizeof(ctypes.c_void_p))
        self.assertIsInstance(detector.is_fullscreen_active(), bool)

    def test_failed_drink_does_not_reset_reminder(self):
        c = self.controller
        previous = c.last_drink
        c.pending_fullscreen_reminder = True
        with patch.object(c.data_manager, "save", side_effect=OSError("locked")):
            with self.assertRaises(OSError):
                c.register_drink()
        self.assertEqual(c.last_drink, previous)
        self.assertTrue(c.pending_fullscreen_reminder)

    def test_menu_interval_selection(self):
        c = self.controller
        c.tray_icon = Mock()
        c.create_tray_menu()
        old = c.tray_menu
        c.set_interval(45)
        self.assertIsNot(c.tray_menu, old)
        menus = [action.menu() for action in c.tray_menu.actions() if action.menu()]
        checked = [action.text() for action in menus[0].actions() if action.isChecked()]
        self.assertEqual(checked, ["45 dakika"])
        c.tray_menu.close()

    def test_startup(self):
        with patch("controller.DataManager", return_value=self.controller.data_manager), \
             patch("controller.QSettings", return_value=Mock(value=Mock(return_value=None))), \
             patch("controller.GoalDialog.exec", return_value=0), \
             patch("controller.QSystemTrayIcon"), \
             patch("controller.QTimer.singleShot"):
            controller = WaterSpiritController(self.app)
        self.assertTrue(controller.reminder_timer.isActive())
        self.assertTrue(controller.activity_timer.isActive())
        self.assertTrue(controller.peek_timer.isActive())
        controller.reminder_timer.stop()
        controller.activity_timer.stop()
        controller.peek_timer.stop()
        controller.window.close()
        controller.peek_window.close()
        controller.tray_menu.close()


if __name__ == "__main__":
    unittest.main()
