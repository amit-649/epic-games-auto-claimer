🎮 Epic Games Auto-Claimer

Hey there! 👋 This is a simple, set-it-and-forget-it tool that grabs the weekly free games from the Epic Games Store for you.

I built this because I kept forgetting to check the store every Thursday. Now, this script runs in the background, checks what's free, and claims it if you don't have it yet.

✨ Why use this?

Never Miss a Freebie: It automatically finds the weekly free games and adds them to your library.

Smart Skipping: It remembers what you already own (using a Google Sheet) so it doesn't waste time trying to claim the same game twice.

Stealth Mode: It runs silently in the background (Headless Mode), so you won't even see a browser window pop up.

Get Notified: Hook it up to Discord, and it'll ping you whenever it grabs a new game. "Success! Just claimed [Game Name]!"

Safe & Secure: It handles age verification gates and skips paid DLCs automatically. Plus, all your login data stays on your own computer.

🚀 Let's Get It Running

Step 1: Grab the Code

Download this project (Click Code -> Download ZIP and unzip it).

Install Python if you don't have it yet (Download Here).

Important: Check the box that says "Add Python to PATH" when installing!

Open the folder in your terminal (Right-click folder -> "Open in Terminal").

Install the necessary libraries by running this command:

``` bash
pip install -r requirements.txt
playwright install chromium
```

Step 2: Give it a Brain (Google Sheets)

We use Google Sheets to keep a log of everything we've claimed.

Go to the Google Cloud Console.

Create a new project (name it whatever you want).

Search for "Google Sheets API" and "Google Drive API" and enable both.

Go to Credentials -> Create Credentials -> Service Account.

Click on the email address it creates, go to Keys -> Add Key -> Create New Key (JSON).

A file will download. Rename it to credentials.json and drop it into your project folder.

Open that JSON file, find the client_email address, and copy it.

Create a new Google Sheet (I call mine "EpicGamesLog") and Share it with that email address (make sure to give it "Editor" access).

Step 3: Configure Your Settings

In the project folder, create a new file named .env.

Open it with Notepad and paste the settings below. Fill in your details!

# --- NOTIFICATIONS (Optional) ---
# Create a Webhook in your Discord Server Settings -> Integrations -> Webhooks
DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE](https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE)

# --- GOOGLE SHEETS SETUP ---
GOOGLE_SHEET_NAME=EpicGamesLog
GOOGLE_CREDENTIALS_FILE=credentials.json

# --- BOT SETTINGS ---
# Set to 'true' to run invisibly, 'false' to watch the browser work
HEADLESS_MODE=true

# How many tabs to open at once? 4 is a sweet spot.
MAX_CONCURRENT_GAMES=4


Step 4: One-Time Login

You need to log in to Epic Games once so the bot saves your session.

Run this command:


```bash
python auth.py
```

A browser window will open. Log in to your Epic account manually.

Once you see the store homepage, head back to your terminal and press Enter.

That's it! Your session is saved safely in the epic_browser_data folder.

Step 5: Launch the Bot 🚀

Time to let it do its thing!

```bash 
python bot.py
```

If everything is set up right, you'll see it scanning for games and logging them to your sheet.

📂 Project Structure

bot.py: The main script. This is where the magic happens.

auth.py: A simple helper to log you in.

.env: Your settings file (Keep this safe!).

credentials.json: Your key to Google Sheets.

epic_browser_data/: Where your login cookies live.

⚠️ A Quick Note

This tool is a fun project for educational purposes. Please use it responsibly and respect Epic Games' Terms of Service. Happy gaming! 🎮