🎮 Epic Games Auto-Claimer Bot

An intelligent, fully automated tool that claims free weekly games from the Epic Games Store for you. It runs in the background, checks for new free games, and claims them if you don't already own them.

✨ What does it do?

Claims Free Games: Automatically finds and claims the weekly free games on Epic.

Skips Owned Games: Checks your Google Sheet history so it doesn't waste time on games you have.

Runs Silently: Can run in "Headless Mode" (invisible) so it doesn't disturb you.

Notifies You: Sends a message to your Discord server when a game is claimed.

Smart & Safe: Handles "Age Verification" gates and avoids claiming paid DLCs by mistake.

🚀 How to Set Up (Step-by-Step)

Step 1: Download and Install

Download this code (Click "Code" -> "Download ZIP" and extract it).

Install Python if you haven't already (Download Python Here). Make sure to check "Add Python to PATH" during installation!

Open the folder in your terminal (Right-click folder -> "Open in Terminal").

Run this command to install the required tools:

pip install -r requirements.txt
playwright install chromium


Step 2: Google Sheets Setup (The "Memory" of the Bot)

Go to the Google Cloud Console.

Create a new project.

Search for "Google Sheets API" and "Google Drive API" and enable both.

Go to Credentials -> Create Credentials -> Service Account.

Click on the email address created, go to Keys -> Add Key -> Create New Key (JSON).

A file will download. Rename it to credentials.json and put it in your project folder.

Open the JSON file, copy the client_email address.

Create a new Google Sheet (name it "EpicGamesLog"), and Share it with that email address (give "Editor" permission).

Step 3: Configuration (The .env File)

In the project folder, create a new text file and name it .env (just .env, no .txt at the end).

Open it with Notepad and paste this inside:

# --- YOUR SECRETS ---
# 1. (Optional) Create a Webhook in your Discord Server Settings -> Integrations -> Webhooks
DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE](https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE)

# 2. The name of the Google Sheet you created
GOOGLE_SHEET_NAME=EpicGamesLog

# 3. The name of your key file (should be credentials.json)
GOOGLE_CREDENTIALS_FILE=credentials.json

# --- SETTINGS ---
# Set to 'true' to run invisibly, 'false' to watch it work
HEADLESS_MODE=true

# How many games to claim at the same time (4 is good for most PCs)
MAX_CONCURRENT_GAMES=4


Step 4: Log In Once

Run this command to log in to your Epic Games account. This saves your session so you don't have to log in every time.

python auth.py


Follow the instructions on screen. Once you are logged in and see the store page, press Enter in the terminal.

Step 5: Run the Bot!

To claim games, simply run:

python bot.py


📂 Files in this Project

bot.py: The main brain. Runs the automation.

auth.py: A helper tool to log you in one time.

.env: (You create this) Stores your settings safely.

credentials.json: (You create this) Your key to Google Sheets.

epic_browser_data/: (Created automatically) Stores your login session.

⚠️ Disclaimer

This tool is for educational purposes. Please use responsibly.
