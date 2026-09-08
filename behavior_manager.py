import random

from messages import MESSAGES


class BehaviorManager:
    def drink_message(
        self,
        drink_result: dict
    ) -> str:
        drink_count = drink_result["drink_count"]
        drink_streak = drink_result["drink_streak"]
        goal = drink_result["goal"]

        if drink_result["rapid_drink"]:
            return random.choice(
                MESSAGES["rapid_drink"]
            )

        if drink_count >= goal:
            return random.choice(
                MESSAGES["goal_complete"]
            )

        remaining = goal - drink_count

        if remaining == 1:
            return random.choice(
                MESSAGES["goal_almost"]
            )

        if drink_count == max(
            1,
            (goal + 1) // 2
        ):
            return random.choice(
                MESSAGES["goal_half"]
            )

        if drink_streak >= 3:
            return random.choice(
                MESSAGES["drink_streak"]
            )

        return random.choice(
            MESSAGES["happy"]
        )

    def snooze_message(
        self,
        snooze_result: dict
    ) -> str:
        consecutive = snooze_result[
            "consecutive_snoozes"
        ]

        if consecutive <= 1:
            category = "snooze_1"

        elif consecutive == 2:
            category = "snooze_2"

        elif consecutive == 3:
            category = "snooze_3"

        else:
            category = "snooze_many"

        return random.choice(
            MESSAGES[category]
        )

    def reminder_message(
        self,
        mood: str
    ) -> str:
        return random.choice(
            MESSAGES[mood]
        )

    def fullscreen_return_message(self) -> str:
        return random.choice(
            MESSAGES["fullscreen_return"]
        )

    def goal_selected_message(
        self,
        goal: int
    ) -> str:
        message = random.choice(
            MESSAGES["goal_selected"]
        )

        return message.format(
            goal=goal
        )

    def peek_caught_message(self) -> str:
        return random.choice(
            MESSAGES["peek_caught"]
        )
