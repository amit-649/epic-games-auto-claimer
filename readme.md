# 🎮 Epic Games Auto-Claimer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![Automation](https://img.shields.io/badge/Automation-Playwright-green?style=flat-square)
![GUI](https://img.shields.io/badge/Interface-Modern%20Dark%20Mode-blueviolet?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Made With Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=flat-square)

**Never miss a free Epic Games title again — automatically, reliably, quietly. 🚀**

Every Thursday, Epic Games drops free games.
And every Thursday… most of us either forget, remember too late, or think *“I’ll claim it later”* — and never do. 😅

This project exists to end that cycle. Permanently.

**Epic Games Auto-Claimer** is an automation tool that runs in the background, checks the store, and claims games for you.

Built from a small personal frustration, but designed with care. Now updated with a **Modern GUI** so you don't need to be a coder to use it!

---

## ✨ Key Features (What Makes This Worth Using)

🖥️ **New: Modern Dark Mode GUI**
No more scary command terminals. Configure everything in a clean, professional app window.

📂 **New: Lite Mode (Zero Setup)**
Don't want to mess with Google Cloud APIs? The bot now defaults to **Lite Mode**, logging all claimed games to a local `history.csv` file automatically.

🧠 **Set & Forget Automation**
Run it weekly. Once configured, it takes care of everything on its own.

🔐 **Automatic Login with 2FA (God Mode)**
Session expired? No problem. The bot can securely log back in using your Epic credentials and TOTP-based 2FA.

☁️ **Google Sheets Logging (Optional)**
Prefer cloud logging? Drop in your `credentials.json`, and the bot automatically syncs with your Google Sheet.

👻 **Headless Background Execution**
Runs silently in headless mode. No browser windows, no interruptions, no distractions.

---

## 📥 How to Download & Run (Easiest Method)

Setup takes about **2 minutes**.

### 1️⃣ Download
Go to the **[Releases Page](../../releases)** and download the latest `.zip` file.

### 2️⃣ Install
Extract the ZIP file to a folder (e.g., `Desktop/EpicBot`).
*⚠️ Important: Do not run it inside the zip file! Extract it first.*

### 3️⃣ Launch
Double-click **`EpicGamesBot.exe`**.

### 4️⃣ Configure & Run
1.  **Fill in your details:** (Epic Email, Password, and 2FA Secret).
2.  Click **SAVE SETTINGS**.
3.  Click **LAUNCH BOT**.

That’s it. You're done.

---

## 🛡️ A Note on Antivirus (False Positives)

Because this bot is built with Python and not digitally signed by a corporation (which costs $$$), **Windows Defender might flag it**.

This is a generic "False Positive" (`Trojan:Win32/Wacatac` etc.) common with all PyInstaller apps.

**You have two choices:**
1.  **Whitelist the folder** in Windows Defender and run the EXE.
2.  **Or, run from source** (instructions below) if you prefer total transparency. The code is open source!

---

## 🐍 How to Run from Source (For Developers)

If you prefer running the raw Python code yourself:

### Prerequisites
*   Python 3.10+
*   Google Chrome installed

### Steps
1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```
3.  Run the GUI:
    ```bash
    python gui.py
    ```

---

## 📊 Google Sheets Setup (Optional)

The bot uses `history.csv` by default. If you want Cloud Logging:

1.  Enable **Sheets API** & **Drive API** in Google Cloud Console.
2.  Download your Service Account Key.
3.  Rename it to `credentials.json` and put it in the bot folder.
4.  Create a Google Sheet named `EpicGamesLog` and share it with the Service Account email.

The bot will automatically detect the file and switch to Cloud Mode.

---

## ⚠️ Disclaimer

This project is intended for **personal automation use only**.
It mimics normal human interaction patterns and does not exploit Epic Games services.

Use responsibly. You are accountable for how you run it.

---

## 🎮 Final Note

This tool exists so you don’t have to think about free games ever again.

Run it.
Schedule it.
Forget about it.

And enjoy your steadily growing Epic Games library. 🎁🎮

**Made with 🩵 by Amit.**