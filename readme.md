![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)
![Automation](https://img.shields.io/badge/Automation-Playwright-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-brightgreen?style=flat-square)
![Made With Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=flat-square)
---

# 🎮 Epic Games Auto-Claimer

**Never miss a free Epic Games title again. Automatically. Reliably. Quietly.**

Every Thursday, Epic Games gives away free games.
And every Thursday, many of us forget to claim them.

This project exists to solve that problem—permanently.

Epic Games Auto-Claimer is a Python automation tool that runs in the background, checks the Epic Games Store for free titles, and claims them for you automatically. No reminders. No manual effort. No missed games.

It also keeps a clean, permanent record of everything you’ve claimed using Google Sheets—so you always know what’s yours.

This tool was built out of a simple frustration, but designed with care, reliability, and respect for automation best practices.

---

## ✨ Key Features

**Set & Forget Automation**
Run it weekly (or schedule it with cron/Task Scheduler). Once configured, it handles everything on its own.

**Automatic Login with 2FA Support**
If your session expires, the bot can securely log in again using Epic Games credentials and TOTP-based 2FA.

**Smart Claim Logic**
Already own a game? The bot detects it and skips unnecessary actions.

**Headless Background Execution**
Runs silently in headless mode. No browser windows, no interruptions.

**Discord Notifications (Optional)**
Receive instant notifications when a new game is successfully claimed.

**Google Sheets Logging**
Every claimed game is recorded in a Google Sheet for long-term tracking.

**Detailed Logging**
All actions, successes, and errors are written to `bot.log` for transparency and debugging.

---

## 🚀 Getting Started

Setup takes approximately **10 minutes**.

### Prerequisites

* Python **3.9+**
* Google account (for Sheets logging)
* Epic Games account
* (Optional) Discord server for notifications

---

## 🛠 Step 1: Installation

1. Download the repository

   * Click **Code → Download ZIP**
   * Extract it to a folder

2. Install Python

   * Download from the official site
   * **Important:** Enable **“Add Python to PATH”** during installation

3. Open a terminal in the project folder

4. Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 📊 Step 2: Google Sheets Setup (Bot Memory)

The bot uses Google Sheets to log claimed games.

1. Open **Google Cloud Console**
2. Create a new project (any name)
3. Enable:

   * Google Sheets API
   * Google Drive API
4. Go to **Credentials → Create Credentials → Service Account**
5. Create a **JSON key**
6. Rename the downloaded file to `credentials.json`
7. Place it in the project root
8. Copy the `client_email` from the JSON file
9. Create a Google Sheet (e.g. `EpicGamesLog`)
10. Share the sheet with that email and grant **Editor access**

---

## ⚙️ Step 3: Configuration

Create a `.env` file in the project directory and configure it as follows:

```env
# --- 🔔 DISCORD NOTIFICATIONS (Optional) ---
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE

# --- 📊 GOOGLE SHEETS ---
GOOGLE_SHEET_NAME=EpicGamesLog
GOOGLE_CREDENTIALS_FILE=credentials.json

# --- 🤖 BOT SETTINGS ---
HEADLESS_MODE=true
MAX_CONCURRENT_GAMES=4

# --- 🔐 AUTO LOGIN (Optional but Recommended) ---
EPIC_EMAIL=your_email@example.com
EPIC_PASSWORD=your_password
EPIC_TOTP_SECRET=YOUR_2FA_SECRET_KEY
```

**Security note:**
Never commit `.env` or `credentials.json` to a public repository.

---

## 🔑 Step 4: Authentication

You have two options:

### Option A: Manual Login (One-Time)

```bash
python auth.py
```

Log in manually once. Cookies will be saved locally.

### Option B: Fully Automated Login (Recommended)

If `EPIC_TOTP_SECRET` is configured, the bot handles login automatically.
No manual step required.

---

## ▶️ Step 5: Run the Bot

```bash
python bot.py
```

If everything is configured correctly, you’ll see success logs and claimed games being recorded.

From this point onward, the bot can be scheduled and forgotten.

---

## 📁 Project Structure

```
bot.py                # Main automation logic
auth.py               # Manual login helper
.env                  # Environment configuration
credentials.json      # Google API credentials
bot.log               # Execution logs
epic_browser_data/    # Stored browser session data
```

---

## ⚠️ Disclaimer

This project is intended for **educational and personal automation use only**.
It mimics normal human interaction patterns and does not exploit Epic Games services.

Use responsibly.
You are accountable for how you run it.

---

## 🎮 Final Note

This tool exists so you don’t have to think about free games ever again.

Run it.
Schedule it.
Forget about it.
Enjoy your growing library.

Happy gaming.
