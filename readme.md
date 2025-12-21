![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)
![Automation](https://img.shields.io/badge/Automation-Playwright-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-brightgreen?style=flat-square)
![Made With Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=flat-square)

# 🎮 Epic Games Auto-Claimer

**Never miss a free Epic Games title again — automatically, reliably, quietly. 🚀**

Every Thursday, Epic Games drops free games.
And every Thursday… most of us either forget, remember too late, or think *“I’ll claim it later”* — and never do. 😅

This project exists to end that cycle. Permanently.

**Epic Games Auto-Claimer** is a Python automation tool that runs in the background, checks the Epic Games Store for free titles, and claims them for you — without reminders, manual clicks, or constant attention.

It also keeps a clean, permanent record of everything you’ve claimed using Google Sheets, so you always know what’s already yours.

Built from a small personal frustration, but designed with care, reliability, and respect for real-world automation practices.

---

## ✨ Key Features (What Makes This Worth Using)

🧠 **Set & Forget Automation**
Run it weekly (or schedule it using cron / Task Scheduler). Once configured, it takes care of everything on its own.

🔐 **Automatic Login with 2FA Support (God Mode)**
Session expired? No problem. The bot can securely log back in using your Epic credentials and TOTP-based 2FA.
No repeated manual logins.

🎯 **Smart Claim Logic**
Already own a game? The bot detects it and skips unnecessary actions — no wasted requests.

👻 **Headless Background Execution**
Runs silently in headless mode. No browser windows, no interruptions, no distractions.

🔔 **Discord Notifications (Optional)**
Get a quick ping on Discord whenever a new game is successfully claimed.

📊 **Google Sheets Logging**
Every claimed title is recorded in a Google Sheet for long-term tracking and peace of mind.

📜 **Detailed Logs**
All actions, successes, and errors are written to `bot.log` for transparency and easy debugging.

---

## 🚀 Getting Started

Setup takes about **10 minutes**.
Grab a coffee ☕ — it’s mostly copy-paste.

---

## 🔧 Prerequisites

* Python **3.9+**
* Google account (for Sheets logging)
* Epic Games account
* (Optional) Discord server for notifications

---

## 🛠 Step 1: Installation

### 1️⃣ Download the repository

* Click **Code → Download ZIP**
* Extract it to a folder

### 2️⃣ Install Python

* Download from the official Python website
* ⚠️ **Important:** Enable **“Add Python to PATH”** during installation

### 3️⃣ Open a terminal in the project folder

Right-click inside the folder → **Open in Terminal**

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

That’s it for setup.

---

## 📊 Step 2: Google Sheets Setup (Bot Memory)

The bot uses Google Sheets to remember what it has already claimed.

1. Open **Google Cloud Console**
2. Create a new project (any name works)
3. Enable:

   * Google Sheets API
   * Google Drive API
4. Go to **Credentials → Create Credentials → Service Account**
5. Create a **JSON key**
6. Rename it to `credentials.json`
7. Place it in the project root folder
8. Open the file and copy the **client_email**
9. Create a Google Sheet (e.g. `EpicGamesLog`)
10. Share the sheet with that email and grant **Editor access**

Once this is done, the bot has a memory.

---

## ⚙️ Step 3: Configuration

Create a `.env` file in the project directory and add the following:

```env
# 🔔 DISCORD NOTIFICATIONS (Optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE

# 📊 GOOGLE SHEETS
GOOGLE_SHEET_NAME=EpicGamesLog
GOOGLE_CREDENTIALS_FILE=credentials.json

# 🤖 BOT SETTINGS
HEADLESS_MODE=true
MAX_CONCURRENT_GAMES=4

# 🔐 AUTO LOGIN (Optional but Recommended)
EPIC_EMAIL=your_email@example.com
EPIC_PASSWORD=your_password
# Epic Account → Password & Security → 2FA → Authenticator App → Manual Entry
EPIC_TOTP_SECRET=YOUR_2FA_SECRET_KEY
```

🔒 **Security note:**
Never commit `.env` or `credentials.json` to a public repository.

---

## 🔑 Step 4: Authentication

You have two choices:

### Option A: Manual Login (One-Time)

```bash
python auth.py
```

Log in once. Cookies are saved locally.

### Option B: Fully Automated Login (Recommended)

If `EPIC_TOTP_SECRET` is configured, the bot handles login automatically.
No manual step needed.

---

## ▶️ Step 5: Run the Bot

```bash
python bot.py
```

If everything is configured correctly, you’ll see success logs and claimed games being recorded.

From this point on, the bot can be scheduled and forgotten.

---

## 📁 Project Structure

```
bot.py                → Main automation logic
auth.py               → Manual login helper
.env                  → Environment configuration
credentials.json      → Google API credentials
bot.log               → Execution logs
epic_browser_data/    → Stored browser session data
```

---

## ⚠️ Disclaimer

This project is intended for **personal and educational automation use only**.
It mimics normal human interaction patterns and does not exploit Epic Games services.

Use responsibly.
You are accountable for how you run it.

---

## 🎮 Final Note

This tool exists so you don’t have to think about free games ever again.

Run it.
Schedule it.
Forget about it.

And enjoy your steadily growing Epic Games library. 🎁🎮

Happy gaming.
