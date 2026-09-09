import sys
import traceback

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox

from app_resources import resource_path
from controller import (
    APP_NAME,
    ORGANIZATION_NAME,
    WaterSpiritController,
)


def main() -> None:
    application = QApplication(
        sys.argv
    )

    application.setApplicationName(
        APP_NAME
    )

    application.setOrganizationName(
        ORGANIZATION_NAME
    )

    application.setWindowIcon(
        QIcon(resource_path("assets/su_cini.ico"))
    )

    application.setQuitOnLastWindowClosed(
        False
    )

    application.setFont(
        QFont(
            "Segoe UI",
            10
        )
    )

    def report_error(error_type, error, tb):
        traceback.print_exception(error_type, error, tb)
        QMessageBox.critical(None, APP_NAME,
            f"İşlem tamamlanamadı. Lütfen tekrar deneyin.\n\n{error}")

    sys.excepthook = report_error
    try:
        controller = WaterSpiritController(application)
    except Exception:
        report_error(*sys.exc_info())
        return

    if controller.shutdown_requested:
        return

    application.water_spirit_controller = (
        controller
    )

    sys.exit(
        application.exec()
    )


if __name__ == "__main__":
    main()
