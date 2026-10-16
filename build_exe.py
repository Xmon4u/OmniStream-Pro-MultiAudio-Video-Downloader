"""
Build standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil

USER_DIR = os.path.dirname(os.path.abspath(__file__))

def build():
    print("=" * 60)
    print("Building NetMirror_MultiAudio_Downloader.exe...")
    print("=" * 60)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "NetMirror_MultiAudio_Downloader",
        "--collect-all", "customtkinter",
        "--add-data", f"{os.path.join(USER_DIR, 'core_engine.py')};.",
        "--add-data", f"{os.path.join(USER_DIR, 'setup_dependencies.py')};.",
        "main_gui.py"
    ]

    result = subprocess.run(cmd, cwd=USER_DIR)
    if result.returncode != 0:
        print("[Error] PyInstaller build failed!")
        return False

    dist_exe = os.path.join(USER_DIR, "dist", "NetMirror_MultiAudio_Downloader.exe")
    if os.path.exists(dist_exe):
        desktop_exe = os.path.join(os.environ["USERPROFILE"], "Desktop", "NetMirror_MultiAudio_Downloader.exe")
        shutil.copy2(dist_exe, desktop_exe)
        print("=" * 60)
        print(f"[SUCCESS] Executable created successfully:")
        print(f"  • User folder: {dist_exe}")
        print(f"  • Desktop:     {desktop_exe}")
        print("=" * 60)
        return True
    return False

if __name__ == "__main__":
    build()
