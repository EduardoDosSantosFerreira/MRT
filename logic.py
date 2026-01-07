import subprocess
from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW


def _silent(command: str):
    startupinfo = STARTUPINFO()
    startupinfo.dwFlags |= STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  # SW_HIDE

    subprocess.Popen(
        command,
        shell=True,
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def run_mrt():
    _silent("mrt")


def run_sfc():
    _silent("sfc /scannow")


def run_dism():
    _silent("DISM /Online /Cleanup-Image /RestoreHealth")


def clean_temp():
    _silent("cleanmgr")
