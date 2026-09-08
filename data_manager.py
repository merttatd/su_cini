import json
import sys
import os
import tempfile
from copy import deepcopy

from datetime import date, datetime
from pathlib import Path
from typing import Any


class DataManager:
    def __init__(self, data_path: Path | None = None) -> None:
        self.data_path = Path(data_path) if data_path is not None else self._get_data_path()
        self.data = self._load_data()
        self._saved_data = deepcopy(self.data)

        self._ensure_default_structure()
        self._reset_daily_values_if_needed()

    def _get_data_path(self) -> Path:
        if sys.platform.startswith("win"):
            folder = (
                Path.home()
                / "AppData"
                / "Roaming"
                / "SuCini"
            )
        else:
            folder = Path.home() / ".su_cini"

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return folder / "data.json"

    def _default_data(self) -> dict[str, Any]:
        return {
            "last_date": date.today().isoformat(),

            "settings": {
                "reminder_interval": 60,
                "daily_goal": 8,
                "cup_size_ml": 250,
            },

            "today": {
                "drink_count": 0,
                "total_ml": 0,
                "snooze_count": 0,
                "drink_streak": 0,
                "consecutive_snoozes": 0,
            },

            "behavior": {
                "last_action": None,
                "last_drink_time": None,
            },

            "history": [],
        }

    def _load_data(self) -> dict[str, Any]:
        if not self.data_path.exists():
            return self._default_data()

        try:
            content = self.data_path.read_text(
                encoding="utf-8"
            )

            loaded = json.loads(content)

            if isinstance(loaded, dict):
                return loaded

        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError
        ):
            pass

        # Preserve unreadable data before writing a replacement.
        backup = self.data_path.with_suffix(".json.corrupt")
        if not backup.exists():
            backup.write_bytes(self.data_path.read_bytes())
        return self._default_data()

    def _ensure_default_structure(self) -> None:
        defaults = self._default_data()

        for key, value in defaults.items():
            if key not in self.data:
                self.data[key] = value

        for section in (
            "settings",
            "today",
            "behavior"
        ):
            default_section = defaults[section]

            if not isinstance(
                self.data.get(section),
                dict
            ):
                self.data[section] = default_section.copy()
                continue

            for key, value in default_section.items():
                self.data[section].setdefault(
                    key,
                    value
                )

        if not isinstance(
            self.data.get("history"),
            list
        ):
            self.data["history"] = []

        for key, default in defaults["settings"].items():
            value = self.data["settings"][key]
            limits = {"daily_goal": (1, 30), "cup_size_ml": (50, 1000),
                      "reminder_interval": (1, 1440)}
            low, high = limits[key]
            if type(value) is not int or not low <= value <= high:
                self.data["settings"][key] = default
        for key in defaults["today"]:
            value = self.data["today"][key]
            if type(value) is not int or value < 0:
                self.data["today"][key] = 0
        self.data["history"] = self.data["history"][-2000:]
        if self.data != self._saved_data:
            self.save()

    def _reset_daily_values_if_needed(self) -> None:
        today_string = date.today().isoformat()

        if self.data.get("last_date") == today_string:
            return

        self.data["last_date"] = today_string

        self.data["today"] = {
            "drink_count": 0,
            "total_ml": 0,
            "snooze_count": 0,
            "drink_streak": 0,
            "consecutive_snoozes": 0,
        }

        self.data["behavior"]["last_action"] = None
        self.data["behavior"]["last_drink_time"] = None

        self.save()

    def save(self) -> None:
        temporary_path = None
        try:
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                    dir=self.data_path.parent, suffix=".tmp", delete=False) as handle:
                temporary_path = Path(handle.name)
                json.dump(self.data, handle, ensure_ascii=False, indent=2)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_path, self.data_path)
            self._saved_data = deepcopy(self.data)
        except OSError:
            self.data = deepcopy(self._saved_data)
            raise
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    def get_setting(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        return self.data["settings"].get(
            key,
            default
        )

    def set_setting(
        self,
        key: str,
        value: Any
    ) -> None:
        limits = {"daily_goal": (1, 30), "cup_size_ml": (50, 1000),
                  "reminder_interval": (1, 1440)}
        if key in limits:
            low, high = limits[key]
            if type(value) is not int or not low <= value <= high:
                raise ValueError(f"Geçersiz ayar: {key}")
        self.data["settings"][key] = value
        self.save()

    def set_daily_goal(
        self,
        goal: int,
        cup_size_ml: int
    ) -> None:
        if type(goal) is not int or not 1 <= goal <= 30:
            raise ValueError("Hedef 1 ile 30 arasında olmalı")
        if type(cup_size_ml) is not int or not 50 <= cup_size_ml <= 1000:
            raise ValueError("Bardak miktarı 50 ile 1000 ml arasında olmalı")
        self.data["settings"]["daily_goal"] = goal
        self.data["settings"]["cup_size_ml"] = cup_size_ml

        self.save()

    def get_daily_goal(self) -> int:
        return int(
            self.get_setting(
                "daily_goal",
                8
            )
        )

    def get_cup_size(self) -> int:
        return int(
            self.get_setting(
                "cup_size_ml",
                250
            )
        )

    def register_drink(self) -> dict[str, Any]:
        self._reset_daily_values_if_needed()
        now = datetime.now()

        today_data = self.data["today"]
        behavior = self.data["behavior"]

        last_drink_text = behavior.get(
            "last_drink_time"
        )

        rapid_drink = False

        if last_drink_text:
            try:
                last_drink = datetime.fromisoformat(
                    last_drink_text
                )

                rapid_drink = 0 <= now.timestamp() - last_drink.timestamp() < 45

            except (ValueError, TypeError, OverflowError, OSError):
                rapid_drink = False

        today_data["drink_count"] += 1
        today_data["total_ml"] += self.get_cup_size()

        if behavior.get("last_action") == "drink":
            today_data["drink_streak"] += 1
        else:
            today_data["drink_streak"] = 1

        today_data["consecutive_snoozes"] = 0

        behavior["last_action"] = "drink"
        behavior["last_drink_time"] = now.isoformat()

        self.data["history"].append(
            {
                "type": "drink",
                "time": now.isoformat(),
                "amount_ml": self.get_cup_size(),
            }
        )

        self.data["history"] = self.data["history"][-2000:]

        self.save()

        return {
            "rapid_drink": rapid_drink,
            "drink_count": today_data["drink_count"],
            "drink_streak": today_data["drink_streak"],
            "total_ml": today_data["total_ml"],
            "goal": self.get_daily_goal(),
        }

    def register_snooze(self) -> dict[str, int]:
        self._reset_daily_values_if_needed()
        now = datetime.now()

        today_data = self.data["today"]
        behavior = self.data["behavior"]

        today_data["snooze_count"] += 1

        if behavior.get("last_action") == "snooze":
            today_data["consecutive_snoozes"] += 1
        else:
            today_data["consecutive_snoozes"] = 1

        today_data["drink_streak"] = 0

        behavior["last_action"] = "snooze"

        self.data["history"].append(
            {
                "type": "snooze",
                "time": now.isoformat(),
            }
        )

        self.data["history"] = self.data["history"][-2000:]

        self.save()

        return {
            "consecutive_snoozes":
                today_data["consecutive_snoozes"],

            "snooze_count":
                today_data["snooze_count"],
        }

    def get_today_stats(self) -> dict[str, int]:
        self._reset_daily_values_if_needed()
        today_data = self.data["today"]

        return {
            "drink_count": int(
                today_data.get(
                    "drink_count",
                    0
                )
            ),

            "total_ml": int(
                today_data.get(
                    "total_ml",
                    0
                )
            ),

            "snooze_count": int(
                today_data.get(
                    "snooze_count",
                    0
                )
            ),

            "goal": self.get_daily_goal(),

            "cup_size_ml": self.get_cup_size(),
        }
