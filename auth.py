from playwright.sync_api import sync_playwright
import os

# Create a folder to store the persistent browser data
USER_DATA_DIR = "./epic_browser_data"

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

def login_and_save_state():
    with sync_playwright() as p:
        print("Launching Real Chrome...")
        
        # Launch persistent context
        # This keeps cookies/cache in the folder you created
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",  # Uses your actual installed Chrome
            headless=False,    # Visible window
            args=["--disable-blink-features=AutomationControlled"] # Hides the "controlled by automation" flag
        )
        
        page = browser.new_page()
        
        print("Navigating to Epic Games Login...")
        page.goto("https://www.epicgames.com/id/login")
        
        print("\n------------------------------------------------")
        print("1. Log in manually. Google Login should work now.")
        print("2. If it still fails, try 'Sign in with Epic Games' (Email/Pass).")
        print("3. Once you are redirected to the STORE HOME PAGE, wait 10 seconds.")
        print("4. Then press ENTER in this terminal to save and exit.")
        print("------------------------------------------------\n")
        
        # Wait for user to press Enter in the terminal
        input("Press ENTER here after you have successfully logged in...")
        
        # Save storage state as a backup (though persistent context saves it automatically)
        browser.storage_state(path="epic_session.json")
        print("Session saved to 'epic_session.json' and persistent folder.")
        
        browser.close()

if __name__ == "__main__":
    login_and_save_state()