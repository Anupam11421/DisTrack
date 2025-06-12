import os
import json
import csv
import random
import time
import threading
from datetime import datetime, timedelta
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel, Label, Entry, Button

# CONFIG
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
SITE_FILE = "sites.json"
LOG_FILE = "logs.txt"
ACCESS_STATS_FILE = "access_stats.txt"
AI_SUGGESTION_LIST = ["facebook.com", "instagram.com", "twitter.com", "netflix.com", "hotstar.com"]

# GLOBALS
current_user = "default"
user_attempts = defaultdict(int)
access_stats = {}
freeze_mode = False
freeze_end_time = None
custom_font = ("Arial", 11)
custom_bg = "#1e1e1e"
custom_fg = "#ffffff"

# MAIN WINDOW
root = tk.Tk()
root.title("WebsiteBlockerPro")
root.geometry("500x550")
root.config(bg=custom_bg)

# UTILITY FUNCTIONS
def log_action(action):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}\n")

def load_sites():
    if not os.path.exists(SITE_FILE):
        with open(SITE_FILE, "w") as f:
            json.dump([], f)
    with open(SITE_FILE, "r") as f:
        return json.load(f)

def save_sites(sites):
    with open(SITE_FILE, "w") as f:
        json.dump(sites, f, indent=4)

# ACCESS ATTEMPTS TRACKING
def track_access_attempt(site):
    if site not in access_stats:
        access_stats[site] = 0
    access_stats[site] += 1
    with open(ACCESS_STATS_FILE, "w") as f:
        for k, v in access_stats.items():
            f.write(f"{k},{v}\n")

# AI SUGGESTION
def ai_suggestion_popup(site):
    suggestions = [
        f"⚠️ Hey! '{site}' looks like a productivity killer.",
        f"👀 Are you sure you want to visit '{site}'? It’s a known distraction.",
        f"🧠 Think twice before opening '{site}' — stay focused!"
    ]
    if site in AI_SUGGESTION_LIST:
        messagebox.showinfo("AI Suggestion", random.choice(suggestions))

# FREEZE MODE
def enable_freeze_mode():
    global freeze_mode, freeze_end_time
    mins = simpledialog.askinteger("Freeze Mode", "Enter minutes to freeze (discipline mode):")
    if mins:
        freeze_mode = True
        freeze_end_time = datetime.now() + timedelta(minutes=mins)
        log_action(f"Freeze Mode ON for {mins} mins")
        messagebox.showinfo("Freeze Mode", f"Blocked for {mins} minutes. Cannot be disabled.")

def check_freeze_mode():
    global freeze_mode, freeze_end_time
    if freeze_mode and datetime.now() >= freeze_end_time:
        freeze_mode = False
        freeze_end_time = None
        log_action("Freeze Mode OFF")
        messagebox.showinfo("Freeze Mode", "You can now unblock sites.")

# BACKUP & RESTORE
def backup_sites():
    path = filedialog.asksaveasfilename(defaultextension=".json")
    if path:
        with open(path, "w") as f:
            json.dump(load_sites(), f, indent=4)
        messagebox.showinfo("Backup", "Sites backed up successfully!")

def restore_sites():
    path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if path:
        with open(path, "r") as f:
            save_sites(json.load(f))
        messagebox.showinfo("Restore", "Sites restored successfully!")

# BLOCKING
def block_sites(duration_minutes=None):
    start_time = time.time()
    while True:
        check_freeze_mode()
        with open(HOSTS_PATH, "r+") as file:
            content = file.read()
            for site in load_sites():
                if site not in content:
                    file.write(REDIRECT_IP + " " + site + "\n")
        if duration_minutes and (time.time() - start_time >= duration_minutes * 60):
            if not freeze_mode:
                unblock_sites()
                break
        time.sleep(10)

def unblock_sites():
    if freeze_mode:
        messagebox.showwarning("Freeze Mode", "Cannot unblock during freeze mode!")
        return
    with open(HOSTS_PATH, "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if not any(site in line for site in load_sites()):
                f.write(line)
        f.truncate()
    log_action("Unblocked all sites")

# GUI CUSTOMIZATION
def customize_gui():
    def apply():
        global custom_bg, custom_font
        try:
            size = int(font_entry.get())
            color = color_entry.get()
            custom_font = ("Arial", size)
            custom_bg = color
            root.config(bg=color)
            update_theme()
            log_action(f"GUI customized: font size {size}, color {color}")
            messagebox.showinfo("Updated", "Customization Applied")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    win = Toplevel(root)
    win.title("Customize GUI")
    Label(win, text="Font Size").pack()
    font_entry = Entry(win)
    font_entry.pack()
    Label(win, text="Background Color (hex)").pack()
    color_entry = Entry(win)
    color_entry.pack()
    Button(win, text="Apply", command=apply).pack()

# THEME SETTING
def update_theme():
    root.config(bg=custom_bg)
    for widget in root.winfo_children():
        try:
            widget.config(bg=custom_bg, fg=custom_fg, font=custom_font)
        except:
            pass

def set_theme():
    global custom_bg, custom_fg
    choice = simpledialog.askstring("Theme", "Type 'light' or 'dark'")
    if choice == "light":
        custom_bg = "#ffffff"
        custom_fg = "#000000"
    else:
        custom_bg = "#1e1e1e"
        custom_fg = "#ffffff"
    update_theme()

# FUNCTIONALITY BUTTONS
def add_site():
    site = entry.get()
    if not site:
        return messagebox.showerror("Error", "Enter a website")
    sites = load_sites()
    if site in sites:
        return messagebox.showinfo("Info", "Already exists")
    ai_suggestion_popup(site)
    sites.append(site)
    save_sites(sites)
    log_action(f"{current_user} added {site}")
    messagebox.showinfo("Added", f"{site} blocked")

def show_sites():
    messagebox.showinfo("Blocked Sites", "\n".join(load_sites()))

def unblock_now():
    unblock_sites()
    messagebox.showinfo("Unblocked", "All sites unblocked")

def block_custom():
    mins = simpledialog.askinteger("Custom Timer", "Block for how many minutes?")
    if mins:
        threading.Thread(target=block_sites, args=(mins,), daemon=True).start()
        log_action(f"{current_user} started block for {mins} minutes")

def export_logs():
    path = filedialog.asksaveasfilename(defaultextension=".csv")
    if path:
        with open(LOG_FILE, "r") as log, open(path, "w", newline='') as out:
            writer = csv.writer(out)
            writer.writerow(["Timestamp", "Action"])
            for line in log:
                if "]" in line:
                    timestamp, action = line.strip().split("]", 1)
                    writer.writerow([timestamp[1:], action.strip()])
        messagebox.showinfo("Exported", "Logs exported")

def switch_user():
    global current_user
    user = simpledialog.askstring("User", "Enter username:")
    if user:
        current_user = user
        log_action(f"Switched user to {user}")
        messagebox.showinfo("User", f"Now using: {user}")

# WIDGETS
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

tk.Button(root, text="➕ Add Website", command=add_site).pack(pady=5)
tk.Button(root, text="🗑 Unblock All", command=unblock_now).pack(pady=5)
tk.Button(root, text="📄 Show Blocked Sites", command=show_sites).pack(pady=5)
tk.Button(root, text="⏱ Custom Block Timer", command=block_custom).pack(pady=5)
tk.Button(root, text="❄️ Freeze Mode", command=enable_freeze_mode).pack(pady=5)
tk.Button(root, text="📦 Backup Sites", command=backup_sites).pack(pady=5)
tk.Button(root, text="📥 Restore Sites", command=restore_sites).pack(pady=5)
tk.Button(root, text="🎨 Customize GUI", command=customize_gui).pack(pady=5)
tk.Button(root, text="🌓 Set Theme", command=set_theme).pack(pady=5)
tk.Button(root, text="📁 Export Logs", command=export_logs).pack(pady=5)
tk.Button(root, text="👤 Switch User", command=switch_user).pack(pady=5)

update_theme()
root.mainloop()
