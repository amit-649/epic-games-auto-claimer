import asyncio
import gspread
import re
import os
import logging
import pyotp
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from playwright.async_api import async_playwright
from datetime import datetime
import sys

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

# --- CONFIGURATION ---
USER_DATA_DIR = os.getenv("BROWSER_DATA_DIR", "./epic_browser_data")
USER_DATA_DIR = os.path.abspath(USER_DATA_DIR)

CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "EpicGamesLog")

try:
    MAX_CONCURRENT_GAMES = int(os.getenv("MAX_CONCURRENT_GAMES", "4"))
except ValueError:
    MAX_CONCURRENT_GAMES = 4

HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() == "true"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# --- GOD MODE CREDENTIALS ---
EPIC_EMAIL = os.getenv("EPIC_EMAIL")
EPIC_PASSWORD = os.getenv("EPIC_PASSWORD")
EPIC_TOTP_SECRET = os.getenv("EPIC_TOTP_SECRET")

# --- LOGGING SETUP ---
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
log_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
if sys.stdout.encoding.lower() != 'utf-8':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.hasHandlers(): logger.handlers.clear()
logger.addHandler(log_handler)
logger.addHandler(console_handler)

# --- GLOBAL VARIABLES ---
gsheet_client = None
gsheet_sheet = None
claimed_cache = set()

def init_sheets():
    global gsheet_client, gsheet_sheet, claimed_cache
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        gsheet_client = gspread.authorize(creds)
        gsheet_sheet = gsheet_client.open(SHEET_NAME).sheet1
        logger.info(f"✅ Connected to Google Sheet: {SHEET_NAME}")
        try:
            urls = gsheet_sheet.col_values(2)
            if urls and urls[0].lower() == "url": urls = urls[1:]
            claimed_cache = set(urls)
            logger.info(f"📚 Loaded {len(claimed_cache)} existing games from sheet.")
        except Exception as e:
            logger.warning(f"⚠️ Could not load cache: {e}")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Google Sheets: {e}")
        gsheet_sheet = None

async def send_discord_notification(context, game_title, game_url, status="Claimed"):
    if not DISCORD_WEBHOOK_URL: return
    color = 5763719 if status == "Claimed" else 15548997
    embed_data = {
        "username": "Epic Games Bot",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/1200px-Epic_Games_logo.svg.png",
        "embeds": [{
            "title": f"🎉 Free Game Status: {game_title}",
            "url": game_url,
            "color": color,
            "fields": [
                {"name": "Status", "value": f"✅ {status}" if status == "Claimed" else f"⚠️ {status}", "inline": True},
                {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True}
            ],
            "footer": {"text": "Automated by Amit's Bot 🚀"}
        }]
    }
    try:
        await context.request.post(DISCORD_WEBHOOK_URL, data=embed_data, headers={"Content-Type": "application/json"})
        logger.info(f"🔔 Rich Discord Notification sent for: {game_title}")
    except Exception as e:
        logger.error(f"⚠️ Failed to send Discord notification: {e}")

def log_to_sheet_sync(game_name: str, url: str, status: str):
    if gsheet_sheet:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            gsheet_sheet.append_row([game_name, url, timestamp, status])
            claimed_cache.add(url)
            logger.info(f"📄 Logged to Google Sheet: {game_name} ({status})")
        except Exception as e:
            logger.error(f"❌ Failed to log: {e}")

async def log_to_sheet(game_name: str, url: str, status: str = "Claimed"):
    await asyncio.to_thread(log_to_sheet_sync, game_name, url, status)

def clean_title(title):
    if not title: return "Unknown Game"
    cleaned = re.sub(r'\s+[a-zA-Z0-9]{6,}$', '', title)
    return cleaned.strip()

# --- ROBUST AUTO-LOGIN FUNCTION ---
async def attempt_auto_login(page):
    logger.info("🤖 Session expired. Attempting God Mode Auto-Login...")
    
    if not EPIC_EMAIL or not EPIC_PASSWORD:
        logger.error("❌ Auto-Login Failed: Missing Credentials in .env")
        return False
        
    try:
        if "/id/login" not in page.url:
             try:
                sign_in_link = page.get_by_role("link", name="Sign In")
                if await sign_in_link.is_visible():
                    await sign_in_link.click()
                    await page.wait_for_load_state("networkidle")
             except: pass

        try:
            epic_login_choice = page.locator("#login-with-epic")
            if await epic_login_choice.is_visible(timeout=5000):
                logger.info("Clicking 'Sign in with Epic Games'...")
                await epic_login_choice.click()
        except: pass

        logger.info("Typing email...")
        email_input = page.locator("input[name='email'], input[type='email']").first
        await email_input.wait_for(state="visible", timeout=10000)
        await email_input.fill(EPIC_EMAIL)
        await email_input.press("Enter")
        await asyncio.sleep(2)
        
        logger.info("Typing password...")
        pass_input = page.locator("input[name='password'], input[type='password']").first
        await pass_input.wait_for(state="visible", timeout=10000)
        await pass_input.fill(EPIC_PASSWORD)
        await pass_input.press("Enter")
        await asyncio.sleep(8) # Wait for processing

        # --- FIX: Use locator() not frame_locator() for counting ---
        if await page.locator("iframe[title*='arkose']").count() > 0 or await page.locator("iframe[src*='arkose']").count() > 0:
            logger.critical("⛔ CAPTCHA DETECTED! Auto-login cannot solve puzzles. Please run auth.py manually.")
            await page.screenshot(path="login_failed_captcha.png")
            return False

        # --- 2FA DETECTION (Broad Search) ---
        logger.info("Scanning for ANY visible 2FA input...")
        otp_input = None
        
        # Poll for 20 seconds
        start_time = datetime.now()
        while (datetime.now() - start_time).seconds < 20:
            # Check all inputs on page
            inputs = page.locator("input:visible")
            count = await inputs.count()
            
            for i in range(count):
                inp = inputs.nth(i)
                # Skip email/password fields if they are still visible
                name = await inp.get_attribute("name") or ""
                type_attr = await inp.get_attribute("type") or ""
                
                if "email" in name or "password" in name or type_attr == "password":
                    continue
                
                # If we found a visible text/tel/number input that ISN'T email/pass, it's likely the OTP
                otp_input = inp
                logger.info(f"Found potential OTP input: name='{name}', type='{type_attr}'")
                break
            
            if otp_input: break
            await asyncio.sleep(1)

        if otp_input:
            if not EPIC_TOTP_SECRET:
                logger.error("❌ 2FA Requested but no Secret Key in .env!")
                return False
                
            logger.info("🔐 Generating 2FA Code...")
            totp = pyotp.TOTP(EPIC_TOTP_SECRET)
            code = totp.now()
            
            await otp_input.fill(code)
            
            continue_btn = page.locator("button[type='submit'], button:has-text('Continue'), button:has-text('Verify')").first
            if await continue_btn.is_visible():
                logger.info("Clicking Continue/Verify...")
                await continue_btn.click()
            else:
                await otp_input.press("Enter")
                
            logger.info("Submitted 2FA Code.")
            
            try:
                logger.info("Waiting for redirect to Store...")
                await page.wait_for_url(re.compile(r"store\.epicgames\.com|epicgames\.com/store"), timeout=30000)
                logger.info("✅ Redirected to Store. Login successful!")
                await asyncio.sleep(5)
                return True
            except:
                logger.error("❌ 2FA Submitted but page did not redirect to Store.")
                await page.screenshot(path="login_failed_2fa_stuck.png")
                return False
            
        logger.info("Verifying login success (No 2FA)...")
        if "/id/login" in page.url:
             logger.error("❌ Still on login URL after attempts. Login failed.")
             await page.screenshot(path="login_stuck_url.png")
             return False

        try:
            await page.wait_for_function("() => !document.querySelector('a[href*=\"/id/login\"]') && !document.querySelector('#login-with-epic')", timeout=10000)
            logger.info("✅ 'Sign In' is gone. Login appears successful!")
            await asyncio.sleep(5)
            return True
        except:
            logger.error("❌ Login Verification Timed Out.")
            await page.screenshot(path="login_failed_final.png")
            return False

    except Exception as e:
        logger.error(f"❌ Auto-Login crashed: {e}")
        try: await page.screenshot(path="login_crash.png")
        except: pass
        return False

async def process_single_game(context, game_url: str, game_title: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        logger.info(f"🚀 Starting Tab: {game_title}")
        page = await context.new_page()
        try:
            await page.goto(game_url, wait_until="domcontentloaded")
            try: await page.wait_for_load_state("networkidle", timeout=3000)
            except: pass

            if "/id/login" in page.url or await page.locator("input[name='email']").is_visible():
                logger.warning(f"⚠️ Redirected to Login on {game_title} tab. Attempting login...")
                success = await attempt_auto_login(page)
                if not success:
                    logger.error(f"❌ Failed to login on tab {game_title}. Closing.")
                    await page.close()
                    return
                # --- FIX: FORCE RELOAD TO APPLY SESSION ---
                logger.info("Refreshing page to apply session...")
                await page.goto(game_url, wait_until="domcontentloaded")
                await asyncio.sleep(5) 

            cta_btn = page.get_by_test_id("purchase-cta-button")
            try:
                await cta_btn.wait_for(state="visible", timeout=20000)
                btn_text_raw = await cta_btn.text_content()
                btn_text = btn_text_raw.lower().strip() if btn_text_raw else ""
                
                if "in library" in btn_text:
                    logger.info(f"✅ Already In Library: {game_title}")
                    await log_to_sheet(game_title, game_url, status="Already Owned")
                    return
                
                if any(x in btn_text for x in ["get", "purchase", "free", "add to cart", "loading"]):
                    if "loading" in btn_text:
                        logger.info("Button says Loading, waiting...")
                        await asyncio.sleep(2)
                        btn_text_raw = await cta_btn.text_content()

                    logger.info(f"👆 Clicking '{btn_text_raw}' ({game_title})...")
                    await cta_btn.click()
                    
                    await asyncio.sleep(2)
                    if "/id/login" in page.url:
                         logger.warning(f"⚠️ Clicked Get -> Redirected to Login. Attempting login...")
                         success = await attempt_auto_login(page)
                         if not success: return
                         # --- FIX: RELOAD AND RE-CLICK ---
                         logger.info("Reloading and re-clicking Get...")
                         await page.goto(game_url, wait_until="domcontentloaded")
                         await asyncio.sleep(5)
                         cta_btn = page.get_by_test_id("purchase-cta-button")
                         await cta_btn.wait_for(state="visible", timeout=10000)
                         await cta_btn.click()

                    logger.info(f"⏳ Waiting for Purchase Modal ({game_title})...")
                    purchase_frame = None
                    for _ in range(30):
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
                            logger.info(f"💰 Placing Order ({game_title})...")
                            await place_order_btn.click()
                            confirmation = page.locator("text=Thanks for your order").or_(page.locator("text=Thank you for buying"))
                            try: await confirmation.wait_for(state="visible", timeout=10000)
                            except:
                                if await place_order_btn.is_visible():
                                    logger.info(f"👉 Retrying Click ({game_title})...")
                                    await place_order_btn.click(force=True)
                                await confirmation.wait_for(state="visible", timeout=30000)
                            
                            logger.info(f"🎉 Claimed Successfully: {game_title}!")
                            await log_to_sheet(game_title, game_url, status="Claimed")
                            await send_discord_notification(context, game_title, game_url, status="Claimed")
                        except Exception as e:
                            logger.error(f"❌ Failed during checkout for {game_title}: {e}")
                            await send_discord_notification(context, game_title, game_url, status="Failed (Checkout)")
                    else:
                        logger.error(f"❌ Purchase frame timed out for {game_title}.")
                        try: await page.screenshot(path=f"debug_no_iframe_{clean_title(game_title)}.png")
                        except: pass
                else:
                    logger.warning(f"⚠️ Unknown Button State '{btn_text}': {game_title}")
                    await log_to_sheet(game_title, game_url, status=f"Skipped - {btn_text}")

            except Exception as e:
                logger.error(f"❌ Error finding button for {game_title}: {e}")
                try: await page.screenshot(path=f"debug_button_error_{clean_title(game_title)}.png")
                except: pass
        except Exception as e:
            logger.error(f"💥 Error processing '{game_title}': {e}")
        finally:
            await page.close()
            logger.info(f"💤 Tab closed: {game_title}")

async def main_job():
    logger.info(f"🚀 Job Started (Async Mode).")
    logger.info(f"📁 Browser Data Dir: {USER_DATA_DIR}")
    init_sheets()

    async with async_playwright() as p:
        try:
            logger.info(f"🌍 Launching Browser (Headless: {HEADLESS_MODE})...")
            launch_args = ["--disable-blink-features=AutomationControlled"]
            if HEADLESS_MODE: launch_args.append("--headless=new")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=HEADLESS_MODE, 
                args=launch_args,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            
            page = context.pages[0] if context.pages else await context.new_page()

            logger.info("🌍 Scanning Free Games List...")
            await page.goto("https://store.epicgames.com/en-US/free-games", wait_until="domcontentloaded")
            
            login_needed = False
            if "/id/login" in page.url:
                login_needed = True
            else:
                try:
                    sign_in_link = page.get_by_role("link", name="Sign In")
                    if await sign_in_link.is_visible():
                        login_needed = True
                except: pass

            if login_needed:
                logger.warning("⚠️ Session Expired! Triggering Auto-Login...")
                success = await attempt_auto_login(page)
                if not success:
                    logger.critical("⛔ Auto-Login Failed. Exiting.")
                    await context.close()
                    return
                await page.goto("https://store.epicgames.com/en-US/free-games", wait_until="domcontentloaded")

            logger.info("⏳ Scrolling to load all items...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(4)

            try: await page.wait_for_selector("span:text('Free Now')", timeout=30000)
            except: logger.warning("Timed out waiting for 'Free Now'.")

            free_now_badges = page.locator("span:text('Free Now')")
            count = await free_now_badges.count()
            logger.info(f"Found {count} elements with 'Free Now' badge.")

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
                    if await title_loc.is_visible(): title = await title_loc.text_content()
                    elif url_raw: title = url_raw.split('/')[-1].replace('-', ' ').title()
                    title = clean_title(title)
                    detected_games.append({"title": title, "url": full_url})
                except Exception: continue

            games_to_process = []
            skipped_count = 0
            for game in detected_games:
                if game['url'] in claimed_cache: skipped_count += 1
                else: games_to_process.append(game)

            if len(games_to_process) == 0:
                logger.info(f"🎉 All {len(detected_games)} detected games are already in your sheet! All Games are Already Claimed!")
            else:
                logger.info(f"📋 Found {len(games_to_process)} new games to process (Skipped {skipped_count} already owned).")
                if DISCORD_WEBHOOK_URL:
                     try: await context.request.post(DISCORD_WEBHOOK_URL, data={"content": f"🚀 **Epic Bot Started:** Found {len(games_to_process)} new games to claim!"})
                     except: pass
                logger.info(f"🔥 Starting parallel processing ({MAX_CONCURRENT_GAMES} tabs at a time)...")
                semaphore = asyncio.Semaphore(MAX_CONCURRENT_GAMES)
                tasks = []
                for game in games_to_process:
                    task = asyncio.create_task(process_single_game(context, game['url'], game['title'], semaphore))
                    tasks.append(task)
                await asyncio.gather(*tasks)
                logger.info("🏁 All tasks completed.")

        except Exception as e:
            logger.critical(f"FATAL ERROR: {e}")
        finally:
             try: await context.close()
             except: pass
             
    print("\n" + "="*40)
    print("Thanks for Using Me, Cr - Amit")
    print("="*40 + "\n")

if __name__ == "__main__":
    asyncio.run(main_job())