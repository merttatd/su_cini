from pathlib import Path
import sys

def resource_path(relative_path: str) -> str:
    """Return a resource path that works in source and PyInstaller builds."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base_path / relative_path)
