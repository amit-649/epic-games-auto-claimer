import asyncio
import gspread
import re
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from playwright.async_api import async_playwright
from datetime import datetime

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

# --- CONFIGURATION (Loaded from .env with Defaults) ---
USER_DATA_DIR = os.getenv("BROWSER_DATA_DIR", "./epic_browser_data")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "EpicGamesLog")

# Convert string from env to integer/boolean
try:
    MAX_CONCURRENT_GAMES = int(os.getenv("MAX_CONCURRENT_GAMES", "4"))
except ValueError:
    MAX_CONCURRENT_GAMES = 4

# Check if headless mode is set to 'true' (case-insensitive)
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() == "true"

# Securely fetch webhook
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# --- GLOBAL VARIABLES ---
gsheet_client = None
gsheet_sheet = None
claimed_cache = set()

# ... (The rest of your script remains exactly the same) ...
def init_sheets():
    global gsheet_client, gsheet_sheet, claimed_cache
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Now using the variable from ENV
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        gsheet_client = gspread.authorize(creds)
        gsheet_sheet = gsheet_client.open(SHEET_NAME).sheet1
        print(f"✅ Connected to Google Sheet: {SHEET_NAME}")
        try:
            urls = gsheet_sheet.col_values(2)
            if urls and urls[0].lower() == "url": urls = urls[1:]
            claimed_cache = set(urls)
            print(f"📚 Loaded {len(claimed_cache)} existing games from sheet.")
        except Exception as e:
            print(f"⚠️ Could not load cache: {e}")
    except Exception as e:
        print(f"❌ Failed to initialize Google Sheets: {e}")
        gsheet_sheet = None

# --- DISCORD NOTIFICATION ---
async def send_discord_notification(context, message):
    if not DISCORD_WEBHOOK_URL: return
    try:
        await context.request.post(DISCORD_WEBHOOK_URL, data={"content": message})
        print(f"🔔 Discord Notification sent: {message}")
    except Exception as e:
        print(f"⚠️ Failed to send Discord notification: {e}")

def log_to_sheet_sync(game_name: str, url: str, status: str):
    global gsheet_sheet, claimed_cache
    if gsheet_sheet:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            gsheet_sheet.append_row([game_name, url, timestamp, status])
            claimed_cache.add(url)
            print(f"📄 Logged to Google Sheet: {game_name} ({status})")
        except Exception as e:
            print(f"❌ Failed to log: {e}")

async def log_to_sheet(game_name: str, url: str, status: str = "Claimed"):
    await asyncio.to_thread(log_to_sheet_sync, game_name, url, status)

def clean_title(title):
    if not title: return "Unknown Game"
    cleaned = re.sub(r'\s+[a-zA-Z0-9]{6,}$', '', title)
    return cleaned.strip()

async def process_single_game(context, game_url: str, game_title: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        print(f"\n🚀 Starting Tab: {game_title}")
        page = await context.new_page()
        
        try:
            await page.goto(game_url, wait_until="domcontentloaded")
            try: await page.wait_for_load_state("networkidle", timeout=3000)
            except: pass

            cta_btn = page.get_by_test_id("purchase-cta-button")
            
            try:
                await cta_btn.wait_for(state="visible", timeout=7000)
                btn_text_raw = await cta_btn.text_content()
                btn_text = btn_text_raw.lower().strip() if btn_text_raw else ""
                
                if "in library" in btn_text:
                    print(f"✅ Already In Library: {game_title}")
                    await log_to_sheet(game_title, game_url, status="Already Owned")
                    return

                if "unavailable" in btn_text or "join waitlist" in btn_text:
                    base_game_warning = page.get_by_text(re.compile(r"(base game required|prerequisite required)", re.IGNORECASE))
                    if await base_game_warning.count() > 0:
                         print(f"⚠️ Base Game Missing: {game_title}")
                         await log_to_sheet(game_title, game_url, status="Skipped - Base Game Missing")
                    else:
                         print(f"⚠️ Unavailable: {game_title}")
                         await log_to_sheet(game_title, game_url, status="Skipped - Unavailable")
                    return

                if any(x in btn_text for x in ["get", "purchase", "free", "add to cart"]):
                    base_game_warning = page.get_by_text(re.compile(r"(base game required|prerequisite required)", re.IGNORECASE))
                    if await base_game_warning.is_visible(timeout=1000):
                         print(f"⚠️ Base Game Warning Detected: {game_title}")
                         await log_to_sheet(game_title, game_url, status="Skipped - Base Game Missing")
                         return

                    print(f"👆 Clicking '{btn_text_raw}' ({game_title})...")
                    await cta_btn.click()
                    
                    print(f"⏳ Waiting for Purchase Modal ({game_title})...")
                    purchase_frame = None
                    for _ in range(15):
                        for frame in page.frames:
                            if "purchase" in frame.url and "highlightColor" in frame.url:
                                purchase_frame = frame
                                break
                        if purchase_frame: break
                        await asyncio.sleep(1)
                    
                    if purchase_frame:
                        try:
                            place_order_btn = purchase_frame.locator("button", has_text="Place Order").first
                            await place_order_btn.wait_for(state="visible", timeout=30000)
                            await asyncio.sleep(2)

                            print(f"💰 Placing Order ({game_title})...")
                            await place_order_btn.click()
                            
                            confirmation = page.locator("text=Thanks for your order").or_(page.locator("text=Thank you for buying"))
                            
                            try:
                                await confirmation.wait_for(state="visible", timeout=5000)
                            except:
                                if await place_order_btn.is_visible():
                                    print(f"👉 Retrying Click ({game_title})...")
                                    await place_order_btn.click(force=True)
                                await confirmation.wait_for(state="visible", timeout=30000)
                            
                            print(f"🎉 Claimed Successfully: {game_title}!")
                            await log_to_sheet(game_title, game_url, status="Claimed")
                            await send_discord_notification(context, f"🎮 **Success!** Claimed free game: **{game_title}**")
                            
                        except Exception as e:
                            print(f"❌ Failed during checkout for {game_title}: {e}")
                            await send_discord_notification(context, f"⚠️ **Error** claiming {game_title}: Checkout failed.")
                    else:
                        print(f"❌ Purchase frame timed out for {game_title}.")
                else:
                    print(f"⚠️ Unknown Button State '{btn_text}': {game_title}")
                    await log_to_sheet(game_title, game_url, status=f"Skipped - {btn_text}")

            except Exception as e:
                continue_btn = page.get_by_role("button", name="Continue", exact=True)
                if await continue_btn.is_visible():
                    print(f"🔞 Age Gate detected. Clicking Continue...")
                    await continue_btn.click()
                    await asyncio.sleep(2)
                    print(f"❌ Age Gate cleared but timed out. Re-run to process.")
                else:
                    print(f"❌ Error finding button for {game_title}: {e}")

        except Exception as e:
            print(f"💥 Error processing '{game_title}': {e}")
        finally:
            await page.close()
            print(f"💤 Tab closed: {game_title}")

async def main_job():
    print(f"\n🚀 [{datetime.now()}] Job Started (Async Mode).")
    init_sheets()

    async with async_playwright() as p:
        try:
            print(f"🌍 Launching Browser (Headless: {HEADLESS_MODE})...")
            
            launch_args = ["--disable-blink-features=AutomationControlled"]
            if HEADLESS_MODE:
                launch_args.append("--headless=new")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=HEADLESS_MODE, 
                args=launch_args,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            
            page = context.pages[0] if context.pages else await context.new_page()

            print("🌍 Scanning Free Games List...")
            await page.goto("https://store.epicgames.com/en-US/free-games", wait_until="domcontentloaded")
            
            sign_in_link = page.get_by_role("link", name="Sign In")
            if await sign_in_link.is_visible():
                print("\n" + "!"*50)
                print("⛔ CRITICAL: YOU ARE LOGGED OUT!")
                print("!"*50 + "\n")
                await context.close()
                return

            print("⏳ Scrolling to load all items...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(4)

            try:
                await page.wait_for_selector("span:text('Free Now')", timeout=30000)
            except:
                print("Timed out waiting for 'Free Now'.")

            free_now_badges = page.locator("span:text('Free Now')")
            count = await free_now_badges.count()
            print(f"Found {count} elements with 'Free Now' badge.")

            detected_games = []
            seen_urls = set()

            for i in range(count):
                try:
                    badge = free_now_badges.nth(i)
                    link = badge.locator("xpath=./ancestor::a[contains(@href, '/p/')]").first
                    if not await link.is_visible(timeout=2000): continue
                    
                    url_raw = await link.get_attribute("href")
                    if not url_raw: continue
                    full_url = f"https://store.epicgames.com{url_raw}"

                    if full_url in seen_urls: continue
                    seen_urls.add(full_url)
                    
                    title = "Unknown Game"
                    title_loc = link.get_by_test_id("offer-card-title").first
                    if await title_loc.is_visible(): 
                        title = await title_loc.text_content()
                    elif url_raw: 
                        title = url_raw.split('/')[-1].replace('-', ' ').title()
                    
                    title = clean_title(title)
                    detected_games.append({"title": title, "url": full_url})

                except Exception:
                    continue

            games_to_process = []
            skipped_count = 0
            
            for game in detected_games:
                if game['url'] in claimed_cache:
                    skipped_count += 1
                else:
                    games_to_process.append(game)

            if len(games_to_process) == 0:
                print(f"\n🎉 All {len(detected_games)} detected games are already in your sheet! All Games are Already Claimed!")
            else:
                print(f"\n📋 Found {len(games_to_process)} new games to process (Skipped {skipped_count} already owned).")
                if DISCORD_WEBHOOK_URL:
                     await send_discord_notification(context, f"🚀 **Epic Bot Started:** Found {len(games_to_process)} new games to claim!")

                print(f"🔥 Starting parallel processing ({MAX_CONCURRENT_GAMES} tabs at a time)...")
                semaphore = asyncio.Semaphore(MAX_CONCURRENT_GAMES)
                tasks = []
                for game in games_to_process:
                    task = asyncio.create_task(process_single_game(context, game['url'], game['title'], semaphore))
                    tasks.append(task)
                
                await asyncio.gather(*tasks)
                print("\n🏁 All tasks completed.")

        except Exception as e:
            print(f"FATAL ERROR: {e}")
        finally:
             try: await context.close()
             except: pass
             
    print("\n" + "="*40)
    print("Thanks for Using Me, Cr - Amit")
    print("="*40 + "\n")

if __name__ == "__main__":
    asyncio.run(main_job())