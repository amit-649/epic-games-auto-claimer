# 🎮 Epic Games Auto-Claimer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Automation-Playwright-green?style=flat-square&logo=playwright&logoColor=white" alt="Playwright" />
  <img src="https://img.shields.io/badge/Cloud-GitHub_Actions_Cron-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Notifications-Discord_Webhook-5865F2?style=flat-square&logo=discord&logoColor=white" alt="Discord" />
  <img src="https://img.shields.io/badge/Interface-Modern%20Dark%20GUI-blueviolet?style=flat-square" alt="GUI" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" alt="Status" />
</p>

**Never miss a free Epic Games title again — automatically, reliably, quietly. 🚀**

Every Thursday, Epic Games drops free games. And every Thursday… most of us either forget, remember too late, or think *"I'll claim it later"* — and never do. 😅

**Epic Games Auto-Claimer** ends that cycle permanently. It can run **locally via a sleek Dark GUI** or **100% in the Cloud via GitHub Actions** so you never even have to turn on your computer!

---

## ⚡ Features & Capabilities

- ☁️ **100% Cloud Automated (GitHub Actions)**: Runs silently in the cloud every Thursday & Friday. Zero CPU, zero battery, zero local runtime.
- 🖥️ **Modern Dark Mode Desktop GUI**: No terminal required if running locally. Configure everything in a clean, professional window.
- 📂 **Lite Mode (Zero Setup)**: Automatically logs claimed games to a local `claimed_games_lite.csv` file without requiring external cloud accounts.
- 🔐 **Automatic Login with TOTP 2FA (God Mode)**: When sessions expire, the bot regenerates real-time 2FA codes and authenticates automatically.
- 🔔 **Discord Webhook Alerts**: Sends instant status briefings to your Discord channel whenever games are detected and claimed.
- ☁️ **Google Sheets Sync (Optional)**: Automatically records claimed titles, redemption timestamps, and game URLs to your Google Sheet.
- 👻 **Stealth Headless Execution**: Employs real user-agent fingerprints and anti-detection flags for reliable claims.

---

## ☁️ 100% Cloud Automated Setup (GitHub Actions)

Run the bot completely free in the cloud without keeping your PC awake:

### 1️⃣ Add Repository Secrets
In your GitHub repository, navigate to **Settings** > **Secrets and variables** > **Actions** and click **New repository secret**:

| Secret Name | Required? | Description |
| :--- | :---: | :--- |
| `EPIC_EMAIL` | **Yes** | Your Epic Games account email |
| `EPIC_PASSWORD` | **Yes** | Your Epic Games account password |
| `EPIC_TOTP_SECRET` | **Yes** | 2FA Secret Key (*Epic Account -> Password & Security -> Two-Factor Authentication -> Authenticator App -> "Manual Entry Key"*)|
| `DISCORD_WEBHOOK_URL` | Optional | Discord Webhook URL for claim alerts |
| `GOOGLE_CREDENTIALS_BASE64` | Optional | Base64-encoded `credentials.json` if syncing to Google Sheets |
| `GOOGLE_SHEET_NAME` | Optional | Defaults to `EpicGamesLog` |

> [!TIP]
> To generate `GOOGLE_CREDENTIALS_BASE64` from your local service account key:
> ```bash
> # In PowerShell:
> [Convert]::ToBase64String([IO.File]::ReadAllBytes("credentials.json")) | Set-Clipboard
> ```

### 2️⃣ Automated Schedule
The included workflow (`.github/workflows/claim_games.yml`) triggers automatically:
- **Every Thursday at 10:00 PM IST (16:30 UTC)**: 30 minutes after Epic Games drops weekly free titles.
- **Every Friday at 10:00 PM IST (16:30 UTC)**: Backup run to guarantee no title is missed.

### 3️⃣ Manual Execution Anytime
Go to the **Actions** tab in your GitHub repository, select **Epic Games Weekly Auto-Claimer**, and click **Run workflow**.

---

## 🖥️ Local Desktop Setup (GUI & Exe)

### 1️⃣ Download Pre-Built Release
1. Go to the **[Releases Page](../../releases)** and download the latest `.zip`.
2. Extract the ZIP to a folder (e.g., `Desktop/EpicBot`).
3. Double-click **`EpicGamesBot.exe`**.
4. Fill in your details (Email, Password, 2FA Secret) and click **LAUNCH BOT**.

---

## 🐍 How to Run from Source (Local Python)

```bash
# Clone the repository
git clone https://github.com/amit-649/epic-games-auto-claimer.git
cd epic-games-auto-claimer

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Launch Modern GUI
python gui.py

# Or run headless bot directly
python bot.py
```

---

## 📊 Google Sheets Setup (Optional)

1. Enable **Google Sheets API** & **Google Drive API** in Google Cloud Console.
2. Download your Service Account JSON key as `credentials.json` into the root directory.
3. Create a Google Sheet named `EpicGamesLog` and share it with the service account email.
4. The bot will automatically detect `credentials.json` and switch from CSV to Cloud Mode.

---

## ⚠️ Disclaimer

This tool is intended for personal automation and game claiming convenience. It respects platform endpoints and does not exploit services.

---

**Made with 🩵 by [Amit Kumar Garai](https://amitcodes.in/).**
