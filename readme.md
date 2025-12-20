🎮 Epic Games Auto-Claimer

Never miss a free game again! 🚀

Hey! 👋 Welcome to my Epic Games Auto-Claimer. I built this tool because, honestly, I kept forgetting to check the Epic Store every Thursday for the free games. And when I did remember, it was usually too late! 😅

So, I wrote this script to do the boring work for me. It runs in the background, checks what's free this week, and claims it automatically. It even tracks everything in a Google Sheet so I know what I've got.

If you're like me and love free stuff but hate the manual work, this is for you. Enjoy! 🎁

✨ Why You'll Love This

😎 Set & Forget: Run it once a week (or schedule it!), and it handles the rest.

🔐 God Mode (Auto-Login): It can log itself in automatically using 2FA if your session expires. No more manual logins!

🧠 Smart Brain: It remembers what you already own, so it won't waste time trying to claim the same game twice.

👻 Ghost Mode: It runs silently in the background (Headless Mode)—you won't even see a browser window open.

🔔 Ding!: Hook it up to your Discord, and get a satisfying notification every time it grabs a new game.

📜 Detailed Logs: Keeps a neat bot.log file so you can see exactly what happened while you were asleep.

🚀 Let's Get Started!

Setting this up takes about 10 minutes. Grab a coffee ☕ and let's go.

Step 1: Download & Install

First things first, let's get the code on your machine.

Download this project (Click the green Code button -> Download ZIP and unzip it).

Install Python if you don't have it.

Important: When installing, check the box that says "Add Python to PATH". Seriously, don't skip this!

Open the folder in your terminal (Right-click inside the folder -> "Open in Terminal").

Run this command to install the required magic spells (libraries):

```bash
pip install -r requirements.txt
playwright install chromium
```

Step 2: Give the Bot a Memory (Google Sheets)

We use Google Sheets to keep a log of everything we've claimed.

Head over to the Google Cloud Console.

Create a New Project (name it "EpicGamesBot" or whatever you like).

Search for "Google Sheets API" and "Google Drive API" and Enable both of them.

Go to Credentials -> Create Credentials -> Service Account.

Click on the email address it creates for you. Go to Keys -> Add Key -> Create New Key (JSON).

A file will download. Rename it to credentials.json and drop it into your project folder.

Open that JSON file, find the client_email line, and copy the email address.

Create a new Google Sheet (I named mine "EpicGamesLog") and Share it with that email address you just copied. (Make sure to give it Editor access!).

Step 3: Configure Your Settings

Now, let's tell the bot how you want it to behave.

In your project folder, create a new file named .env.

Open it with Notepad (or VS Code) and paste in these settings.

Fill in your details!

# --- 🔔 NOTIFICATIONS (Optional) ---
# Want a ping on Discord? Create a Webhook in Server Settings -> Integrations -> Webhooks
DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE](https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE)

# --- 📊 GOOGLE SHEETS SETUP ---
GOOGLE_SHEET_NAME=EpicGamesLog
GOOGLE_CREDENTIALS_FILE=credentials.json

# --- 🤖 BOT SETTINGS ---
# Set to 'true' to run invisibly, 'false' if you want to watch the browser work (it's oddly satisfying)
HEADLESS_MODE=true

# How many games/tabs to process at once? 4 is usually a safe bet.
MAX_CONCURRENT_GAMES=4

# --- 🔐 GOD MODE (Auto-Login) ---
# If you want the bot to login automatically when cookies expire:
EPIC_EMAIL=your_email@example.com
EPIC_PASSWORD=your_password
# Get this from Epic Account -> Password & Security -> 2FA -> Authenticator App -> "Manual Entry"
EPIC_TOTP_SECRET=YOUR_2FA_SECRET_KEY_HERE


Step 4: The One-Time Login (Or Just Run It!)

You have two choices:

Manual Login: Run python auth.py to log in once manually.

God Mode: If you filled in the EPIC_TOTP_SECRET in your .env file, the bot can log in by itself! You can just skip to Step 5.

Step 5: Launch It! 🚀

The moment of truth. Run the bot and watch it go!

```bash
python bot.py
```

If you see green text and "Success!" messages, you're all set. Sit back and enjoy your free games. 🎉

📂 What's inside?

bot.py: The main brain. This runs the show.

auth.py: A helper tool for manual login.

.env: Your settings file (Keep this safe!).

credentials.json: Your key to Google Sheets.

bot.log: A text file where the bot writes down everything it does (errors, successes, etc.).

epic_browser_data/: Where your login cookies live.

⚠️ Just a Heads Up

This tool is a fun hobby project for educational purposes. Use it responsibly! I'm not responsible if Epic Games gets mad (though this script tries to be very polite and human-like).

Happy Gaming! 🎮