# NetMi.Video Downloader - Build Script
# Compiles a standalone Windows .exe using PyInstaller.

import os
import sys
import subprocess
import shutil

USER_DIR  = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(USER_DIR, "app_icon.ico")
EXE_NAME  = "NetMi_Video_Downloader"


def build():
    print("=" * 60)
    print(f"Building {EXE_NAME}.exe ...")
    print("=" * 60)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", EXE_NAME,
        "--icon", ICON_PATH,
        "--collect-all", "customtkinter",
        "--add-data", os.path.join(USER_DIR, "core_engine.py") + ";.",
        "--add-data", os.path.join(USER_DIR, "setup_dependencies.py") + ";.",
        "--add-data", ICON_PATH + ";.",
        "main_gui.py",
    ]

    result = subprocess.run(cmd, cwd=USER_DIR)
    if result.returncode != 0:
        print("[Error] PyInstaller build failed!")
        return False

    dist_exe = os.path.join(USER_DIR, "dist", EXE_NAME + ".exe")
    if os.path.exists(dist_exe):
        desktop_exe = os.path.join(
            os.environ.get("USERPROFILE", os.path.expanduser("~")),
            "Desktop", EXE_NAME + ".exe"
        )
        shutil.copy2(dist_exe, desktop_exe)
        size_mb = os.path.getsize(desktop_exe) / (1024 * 1024)
        print("=" * 60)
        print(f"[SUCCESS] {EXE_NAME}.exe is ready!")
        print(f"  Location: {desktop_exe}")
        print(f"  Size    : {size_mb:.1f} MB")
        print("=" * 60)
        return True

    print("[Error] Executable not found after build.")
    return False


if __name__ == "__main__":
    build()
