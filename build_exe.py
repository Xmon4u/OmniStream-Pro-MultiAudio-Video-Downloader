"""
Build standalone executable using PyInstaller with custom app icon
"""

import os
import sys
import subprocess
import shutil

USER_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(USER_DIR, "app_icon.ico")
EXE_NAME = "Ultra_Downloader_MultiAudio"

def build():
    print("=" * 60)
    print(f"Building {EXE_NAME}.exe with custom icon...")
    print("=" * 60)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", EXE_NAME,
        "--icon", ICON_PATH,
        "--collect-all", "customtkinter",
        "--add-data", f"{os.path.join(USER_DIR, 'core_engine.py')};.",
        "--add-data", f"{os.path.join(USER_DIR, 'setup_dependencies.py')};.",
        "--add-data", f"{ICON_PATH};.",
        "main_gui.py"
    ]

    result = subprocess.run(cmd, cwd=USER_DIR)
    if result.returncode != 0:
        print("[Error] PyInstaller build failed!")
        return False

    dist_exe = os.path.join(USER_DIR, "dist", f"{EXE_NAME}.exe")
    if os.path.exists(dist_exe):
        desktop_exe = os.path.join(os.environ["USERPROFILE"], "Desktop", f"{EXE_NAME}.exe")
        shutil.copy2(dist_exe, desktop_exe)
        print("=" * 60)
        print(f"[SUCCESS] Executable created successfully:")
        print(f"  • Dist folder: {dist_exe}")
        print(f"  • Desktop:     {desktop_exe}")
        print("=" * 60)
        return True
    return False

if __name__ == "__main__":
    build()
