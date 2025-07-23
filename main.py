import os
import time
import random
import string
import threading
import sys
import requests

# ───── Colors ─────
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

RUNNING_DIR = "running_tasks"
SENT_LOG = "sent_messages.txt"
os.makedirs(RUNNING_DIR, exist_ok=True)

def generate_key():
    return "BROKENNADEEM-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def animate_text(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def parse_cookie(cookie_str):
    cookies = {}
    for part in cookie_str.split(";"):
        if "=" in part:
            key, value = part.strip().split("=", 1)
            cookies[key] = value
    return cookies

def send_message(cookie_str, convo_id, message):
    cookies = parse_cookie(cookie_str)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": f"https://www.facebook.com/messages/t/{convo_id}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "fb_dtsg": "",  # Optional, FB sometimes doesn't need it if session is active
        "body": message,
        "tids": f"cid.c.{convo_id}",
        "wwwupp": "C3",
        "csid": str(random.randint(1111111, 9999999)),
        "offline_threading_id": str(random.randint(1111111111111, 9999999999999)),
        "source": "source:chat:web",
        "client": "mercury"
    }

    try:
        r = requests.post("https://www.facebook.com/messages/send/", headers=headers, cookies=cookies, data=data)
        if r.status_code == 200 and 'error' not in r.text:
            return True
        else:
            return False
    except Exception as e:
        print(RED + f"❌ Request error: {e}" + RESET)
        return False

def start_loader():
    print()
    animate_text(CYAN + "🍪 Enter FULL DESKTOP COOKIE:" + RESET)
    cookie = input("➤ ").strip()

    animate_text(CYAN + "💬 Enter CONVERSATION ID (not UID):" + RESET)
    convo_id = input("➤ ").strip()

    animate_text(CYAN + "📁 Enter MESSAGE FILE path:" + RESET)
    msg_file = input("➤ ").strip()
    if not os.path.exists(msg_file):
        print(RED + "❌ Message file not found!" + RESET)
        return

    animate_text(CYAN + "⏱️ Enter speed in seconds (e.g. 2):" + RESET)
    try:
        delay = float(input("➤ ").strip())
    except:
        delay = 2.0

    key = generate_key()
    task_file = os.path.join(RUNNING_DIR, key)
    open(task_file, "w").close()

    def run_task():
        with open(msg_file, "r") as f:
            messages = [line.strip() for line in f if line.strip()]
        while os.path.exists(task_file):
            for msg in messages:
                if not os.path.exists(task_file):
                    break
                sent = send_message(cookie, convo_id, msg)
                if sent:
                    print(GREEN + f"✔ Sent: {msg}" + RESET)
                    with open(SENT_LOG, "a") as log:
                        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {msg}\n")
                else:
                    print(RED + f"❌ Failed to send: {msg}" + RESET)
                time.sleep(delay)

    threading.Thread(target=run_task, daemon=True).start()
    print(GREEN + f"\n✅ Started! Stop key: {key}" + RESET)

def stop_loader():
    animate_text(CYAN + "🔑 Enter your STOP KEY:" + RESET)
    key = input("➤ ").strip()
    path = os.path.join(RUNNING_DIR, key)
    if os.path.exists(path):
        os.remove(path)
        print(GREEN + "🛑 Task stopped." + RESET)
    else:
        print(RED + "❌ Key not found." + RESET)

def show_menu():
    while True:
        print(CYAN)
        print("██████╗░██████╗░░█████╗░██╗░░██╗███████╗███╗░░██╗")
        print("██╔══██╗██╔══██╗██╔══██╗██║░░██║██╔════╝████╗░██║")
        print("██║░░██║██████╦╝██║░░██║███████║█████╗░░██╔██╗██║")
        print("██║░░██║██╔══██╗██║░░██║██╔══██║██╔══╝░░██║╚████║")
        print("██████╔╝██████╦╝╚█████╔╝██║░░██║███████╗██║░╚███║")
        print("╚═════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝")
        print(YELLOW + "🧠 REAL COOKIE MESSENGER BY BROKEN NADEEM 🧠" + RESET)
        print(GREEN + "\n1️⃣  START LOADER\n2️⃣  STOP LOADER\n3️⃣  EXIT" + RESET)
        choice = input("➤ Choose option: ").strip()
        if choice == "1":
            start_loader()
        elif choice == "2":
            stop_loader()
        elif choice == "3":
            break
        else:
            print(RED + "❌ Invalid option!" + RESET)
        input(YELLOW + "\n🔁 Press ENTER to continue..." + RESET)

if __name__ == "__main__":
    show_menu()
