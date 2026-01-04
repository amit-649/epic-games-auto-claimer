import customtkinter as ctk
import threading
import asyncio
import sys
import logging
import os
import webbrowser
from dotenv import set_key, load_dotenv

# Import your bot logic
import bot

# --- THEME CONFIGURATION (Epic Games Style) ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # We will override this with custom colors

# Colors
COLOR_BG = "#121212"          # Main Window Background
COLOR_SIDEBAR = "#202020"     # Sidebar Background
COLOR_ACCENT = "#0078F2"      # Epic Blue
COLOR_ACCENT_HOVER = "#005CB8"
COLOR_TEXT_ENTRY = "#2A2A2A"  # Darker gray for input fields
COLOR_TEXT_WHITE = "#F5F5F5"
COLOR_TEXT_GRAY = "#9E9E9E"

class TextRedirector:
    """Redirects print statements to the GUI Textbox"""
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, string):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", string)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass

class EpicBotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("Epic Games Claimer")
        self.geometry("950x650")
        self.configure(fg_color=COLOR_BG)
        
        # Load current settings
        load_dotenv()

        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =================================================
        # SIDEBAR (Settings & Controls)
        # =================================================
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1) # Spacer to push footer down

        # Header
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="EPIC BOT", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=COLOR_TEXT_WHITE
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        # --- INPUT FIELDS ---
        self.create_label("Epic Email", 1)
        self.entry_email = self.create_entry(os.getenv("EPIC_EMAIL", ""), 2)

        self.create_label("Epic Password", 3)
        
        # Password Frame for toggle
        self.pass_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.pass_frame.grid(row=4, column=0, padx=20, pady=0, sticky="ew")
        
        self.entry_pass = ctk.CTkEntry(
            self.pass_frame,
            placeholder_text="Password",
            show="*", 
            fg_color=COLOR_TEXT_ENTRY,
            border_width=0,
            height=35,
            text_color="white"
        )
        self.entry_pass.pack(side="left", fill="x", expand=True)
        self.entry_pass.insert(0, os.getenv("EPIC_PASSWORD", ""))

        # Show Pass Checkbox (Styled like a small toggle)
        self.check_show_pass = ctk.CTkCheckBox(
            self.pass_frame, 
            text="Show", 
            width=50,
            command=self.toggle_password,
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_GRAY,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER
        )
        self.check_show_pass.pack(side="right", padx=(10, 0))

        self.create_label("2FA Secret (Optional)", 5)
        self.entry_2fa = self.create_entry(os.getenv("EPIC_TOTP_SECRET", ""), 6)
        
        self.create_label("Discord Webhook", 7)
        self.entry_webhook = self.create_entry(os.getenv("DISCORD_WEBHOOK_URL", ""), 8)

        # Headless Switch
        self.switch_headless = ctk.CTkSwitch(
            self.sidebar, 
            text="Headless Mode",
            font=ctk.CTkFont(size=12, weight="bold"),
            progress_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_WHITE
        )
        self.switch_headless.grid(row=9, column=0, padx=20, pady=20, sticky="w")
        if os.getenv("HEADLESS_MODE", "True").lower() == "true":
            self.switch_headless.select()

        # --- BUTTONS ---
        self.btn_save = ctk.CTkButton(
            self.sidebar, 
            text="SAVE SETTINGS", 
            command=self.save_settings, 
            fg_color="#333333", 
            hover_color="#444444",
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_save.grid(row=11, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.btn_start = ctk.CTkButton(
            self.sidebar, 
            text="LAUNCH BOT", 
            command=self.start_bot_thread, 
            fg_color=COLOR_ACCENT, 
            hover_color=COLOR_ACCENT_HOVER,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.btn_start.grid(row=12, column=0, padx=20, pady=(0, 20), sticky="ew")

        # --- FOOTER ---
        self.footer_label = ctk.CTkLabel(
            self.sidebar, 
            text="Made by Amit with 🩵", 
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_GRAY
        )
        self.footer_label.grid(row=13, column=0, padx=20, pady=(0, 20))

        # =================================================
        # MAIN AREA (Logs & Report)
        # =================================================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Top Bar in Main Area
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            self.top_frame, 
            text="SYSTEM LOGS", 
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=COLOR_TEXT_GRAY
        ).pack(side="left")

        # Report Error Button (Small, Red/Orange)
        self.btn_report = ctk.CTkButton(
            self.top_frame,
            text="⚠️ Report Issue",
            command=self.report_issue,
            width=100,
            height=25,
            fg_color="#D83C3E", # Epic Error Red
            hover_color="#B32D2F",
            font=ctk.CTkFont(size=11)
        )
        self.btn_report.pack(side="right")

        # Log Box (Terminal Style)
        self.textbox_log = ctk.CTkTextbox(
            self.main_frame, 
            font=("Consolas", 12),
            fg_color="#000000",
            text_color="#00FF00", # Matrix/Hacker green for logs
            corner_radius=5
        )
        self.textbox_log.grid(row=1, column=0, sticky="nsew")
        self.textbox_log.configure(state="disabled")

        # Redirect Console
        sys.stdout = TextRedirector(self.textbox_log)
        sys.stderr = TextRedirector(self.textbox_log)
        
        # Attach GUI handler to the logger
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        bot.logger.addHandler(log_handler)

    # --- HELPER FUNCTIONS ---
    def create_label(self, text, row):
        label = ctk.CTkLabel(
            self.sidebar, 
            text=text, 
            anchor="w", 
            text_color=COLOR_TEXT_GRAY,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        label.grid(row=row, column=0, padx=20, pady=(10, 0), sticky="w")

    def create_entry(self, default_val, row):
        entry = ctk.CTkEntry(
            self.sidebar, 
            fg_color=COLOR_TEXT_ENTRY,
            border_width=0,
            height=35,
            text_color="white"
        )
        entry.grid(row=row, column=0, padx=20, pady=(5, 0), sticky="ew")
        entry.insert(0, default_val)
        return entry

    def toggle_password(self):
        if self.check_show_pass.get() == 1:
            self.entry_pass.configure(show="")
        else:
            self.entry_pass.configure(show="*")

    def save_settings(self):
        set_key(".env", "EPIC_EMAIL", self.entry_email.get())
        set_key(".env", "EPIC_PASSWORD", self.entry_pass.get())
        set_key(".env", "EPIC_TOTP_SECRET", self.entry_2fa.get())
        set_key(".env", "DISCORD_WEBHOOK_URL", self.entry_webhook.get())
        set_key(".env", "HEADLESS_MODE", str(self.switch_headless.get() == 1))
        print("✅ Settings Saved to .env")

    def report_issue(self):
        # UPDATE THIS URL TO YOUR GITHUB REPO ISSUES PAGE
        github_issues_url = "https://github.com/amit-649/epic-games-auto-claimer/issues/new"
        print(f"🔗 Opening Report Page: {github_issues_url}")
        webbrowser.open(github_issues_url)

    def start_bot_thread(self):
        self.btn_start.configure(state="disabled", text="RUNNING...", fg_color="#333333")
        thread = threading.Thread(target=self.run_bot)
        thread.start()

    def run_bot(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot.main_job())
            loop.close()
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
        finally:
            self.btn_start.configure(state="normal", text="LAUNCH BOT", fg_color=COLOR_ACCENT)

if __name__ == "__main__":
    app = EpicBotGUI()
    app.mainloop()