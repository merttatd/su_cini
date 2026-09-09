import sys


class ActivityDetector:
    def __init__(self) -> None:
        self.is_windows = (
            sys.platform.startswith("win")
        )

        if not self.is_windows:
            return

        try:
            import ctypes
            from ctypes import wintypes

            self.ctypes = ctypes
            self.wintypes = wintypes

            self.user32 = ctypes.windll.user32
            # Explicit signatures preserve 64-bit HWND/HMONITOR handles.
            for name in ("GetForegroundWindow", "GetDesktopWindow", "GetShellWindow"):
                function = getattr(self.user32, name)
                function.argtypes = []
                function.restype = wintypes.HWND
            self.user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
            self.user32.GetWindowRect.restype = wintypes.BOOL
            self.user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
            self.user32.MonitorFromWindow.restype = wintypes.HANDLE
            self.monitor_info_type = self.MONITORINFO
            self.user32.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(self.monitor_info_type)]
            self.user32.GetMonitorInfoW.restype = wintypes.BOOL

        except (
            ImportError,
            AttributeError
        ):
            self.is_windows = False

    def is_fullscreen_active(self) -> bool:
        if not self.is_windows:
            return False

        try:
            foreground_window = (
                self.user32.GetForegroundWindow()
            )

            if not foreground_window:
                return False

            if self._is_desktop_window(
                foreground_window
            ):
                return False

            window_rect = self.wintypes.RECT()

            if not self.user32.GetWindowRect(
                foreground_window,
                self.ctypes.byref(window_rect)
            ):
                return False

            monitor = self.user32.MonitorFromWindow(
                foreground_window,
                2
            )

            if not monitor:
                return False

            monitor_info = self.monitor_info_type()
            monitor_info.cbSize = self.ctypes.sizeof(
                self.monitor_info_type
            )

            if not self.user32.GetMonitorInfoW(
                monitor,
                self.ctypes.byref(monitor_info)
            ):
                return False

            monitor_rect = monitor_info.rcMonitor

            tolerance = 3

            covers_left = (
                window_rect.left
                <= monitor_rect.left + tolerance
            )

            covers_top = (
                window_rect.top
                <= monitor_rect.top + tolerance
            )

            covers_right = (
                window_rect.right
                >= monitor_rect.right - tolerance
            )

            covers_bottom = (
                window_rect.bottom
                >= monitor_rect.bottom - tolerance
            )

            return (
                covers_left
                and covers_top
                and covers_right
                and covers_bottom
            )

        except Exception:
            return False

    @property
    def MONITORINFO(self):
        class MonitorInfo(
            self.ctypes.Structure
        ):
            _fields_ = [
                (
                    "cbSize",
                    self.wintypes.DWORD
                ),
                (
                    "rcMonitor",
                    self.wintypes.RECT
                ),
                (
                    "rcWork",
                    self.wintypes.RECT
                ),
                (
                    "dwFlags",
                    self.wintypes.DWORD
                ),
            ]

        return MonitorInfo

    def _is_desktop_window(
        self,
        window_handle
    ) -> bool:
        desktop_window = (
            self.user32.GetDesktopWindow()
        )

        shell_window = (
            self.user32.GetShellWindow()
        )

        return window_handle in (
            desktop_window,
            shell_window
        )
