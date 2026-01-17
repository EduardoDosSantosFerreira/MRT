import sys
import ctypes
from PySide6.QtWidgets import QApplication
from ui import SecurityTool


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def relaunch_as_admin():
    params = " ".join(sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit()


if not is_admin():
    relaunch_as_admin()


def main():
    app = QApplication(sys.argv)
    window = SecurityTool()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
