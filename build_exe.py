import PyInstaller.__main__
import os
import shutil

# Clean previous build
if os.path.exists("dist"): shutil.rmtree("dist")
if os.path.exists("build"): shutil.rmtree("build")

print("🚧 Building Epic Games Bot...")

PyInstaller.__main__.run([
    'gui.py',
    '--name=EpicGamesBot',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--hidden-import=gspread',
    '--hidden-import=oauth2client',
    '--collect-all=customtkinter',
    
    # ADD THIS LINE HERE:
    '--version-file=file_version_info.txt',
    
    '--icon=NONE' 
])

print("\n✅ Build Complete!")