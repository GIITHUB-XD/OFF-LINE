import os
import time
import random
import string
import threading
import sys
import subprocess
import json
import requests

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

RUNNING_DIR = "running_tasks"
SENT_LOG = "sent_messages.txt"
BLOCKED_LOG = "blocked_tokens.txt"
os.makedirs(RUNNING_DIR, exist_ok=True)

def generate_key():
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return f"BROKENNADEEM-{rand}"

def animate_text(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def keep_awake():
    try:
        subprocess.call(['termux-wake-lock'])
    except:
        pass

def is_valid_user_token(token):
    return token.startswith("EAAD") or token.startswith("EAAB") or token.startswith("EAAZ")

def send_message(token, convo_id, message):
    url = f"https://graph.facebook.com/v19.0/{convo_id}/messages"
    payload = {
        "messaging_type": "RESPONSE",
        "message": {"text": message},
        "access_token": token
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if "error" in data:
            code = data["error"].get("code")
            if code == 368:
                return "blocked"
            return "error"
        return "sent"
    except Exception:
        return "network"

def start_loader():
    keep_awake()
    print()
    animate_text(CYAN + "🔐 Enter path to TOKEN FILE (EAAD only):" + RESET)
    print("──────────────────────────────")
    token_file = input("➤ ").strip()
    if not os.path.isfile(token_file):
        print(RED + "❌ Token file not found!" + RESET)
        return

    animate_text(CYAN + "💬 Enter CONVERSATION UID:" + RESET)  
    print("──────────────────────────────")  
    convo_id = input("➤ ").strip()  
    if not convo_id:  
        print(RED + "❌ Invalid Convo ID!" + RESET)  
        return  

    animate_text(CYAN + "😡 Enter HATER NAME:" + RESET)  
    print("──────────────────────────────")  
    hater_name = input("➤ ").strip()  

    animate_text(CYAN + "📁 Enter path to MESSAGE FILE:" + RESET)  
    print("──────────────────────────────")  
    message_file = input("➤ ").strip()  
    if not os.path.isfile(message_file):  
        print(RED + "❌ Message file not found!" + RESET)  
        return  

    animate_text(CYAN + "⏱️ Enter SPEED in seconds (recommended: 5–10):" + RESET)  
    print("──────────────────────────────")  
    try:  
        speed = float(input("➤ ").strip())  
    except:  
        speed = 5.0

    key = generate_key()  
    task_file = os.path.join(RUNNING_DIR, key)  
    open(task_file, 'w').close()  

    def run_task():  
        blocked = []

        with open(token_file, 'r') as tf:  
            tokens = [line.strip() for line in tf if line.strip() and is_valid_user_token(line.strip())]

        if not tokens:
            print(RED + "❌ No valid EAAD user tokens found!" + RESET)
            os.remove(task_file)
            return

        with open(message_file, 'r') as mf:  
            messages = [line.strip() for line in mf if line.strip()]  

        for token in tokens:
            token_blocked = False
            for msg in messages:  
                if not os.path.isfile(task_file):  
                    print(RED + f"\n⛔ Task stopped: {key}" + RESET)  
                    return  
                full_msg = f"@{hater_name} {msg}"  
                result = send_message(token, convo_id, full_msg)
                if result == "sent":
                    with open(SENT_LOG, 'a') as log:  
                        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {hater_name} ➤ {msg}\n")  
                    print(GREEN + f"✔ Sent: {msg}" + RESET)  
                    time.sleep(speed)
                elif result == "blocked":
                    print(RED + "⛔ Blocked Token Detected (code 368). Skipping." + RESET)
                    token_blocked = True
                    blocked.append(token)
                    break
                elif result == "network":
                    print(RED + "🌐 Network error. Retrying..." + RESET)
                    time.sleep(3)
                else:
                    print(YELLOW + f"⚠️ Error sending message. Skipping message." + RESET)
                    time.sleep(2)

        if blocked:
            with open(BLOCKED_LOG, 'a') as bfile:
                for b in blocked:
                    bfile.write(b + "\n")
            print(RED + f"\n⛔ {len(blocked)} token(s) blocked. Logged to {BLOCKED_LOG}" + RESET)

    threading.Thread(target=run_task, daemon=True).start()  
    print(GREEN + f"\n✅ Loader Started Successfully!" + RESET)  
    time.sleep(0.5)  
    print(YELLOW + f"🆔 Your UNIQUE STOP KEY: {key}" + RESET)  
    time.sleep(0.5)  
    print(CYAN + "⚠️ Use Option 2 to stop using this key." + RESET)  
    time.sleep(0.5)  
    print(CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" + RESET)

def stop_loader():
    animate_text(CYAN + "\n🔑 Enter your UNIQUE STOP KEY:" + RESET)
    print("──────────────────────────────")
    key = input("➤ ").strip()
    task_path = os.path.join(RUNNING_DIR, key)
    if os.path.isfile(task_path):
        os.remove(task_path)
        print(GREEN + f"🛑 Requested to stop task with key: {key}" + RESET)
    else:
        print(RED + "❌ Key not found or already stopped!" + RESET)

def display_sms():
    print("\n" + CYAN + "📜 Sent Messages Log:" + RESET)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if os.path.isfile(SENT_LOG):
        with open(SENT_LOG, 'r') as log:
            print(log.read())
    else:
        print(YELLOW + "📭 No messages sent yet." + RESET)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def show_logo():
    os.system("clear" if os.name == "posix" else "cls")
    print(CYAN)
    print("███╗░░██╗░█████╗░██████╗░███████╗███████╗███╗░░██╗")
    print("████╗░██║██╔══██╗██╔══██╗██╔════╝██╔════╝████╗░██║")
    print("██╔██╗██║███████║██████╔╝█████╗░░█████╗░░██╔██╗██║")
    print("██║╚████║██╔══██║██╔═══╝░██╔══╝░░██╔══╝░░██║╚████║")
    print("██║░╚███║██║░░██║██║░░░░░███████╗███████╗██║░╚███║")
    print("╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚══════╝╚═╝░░╚══╝")
    print("   💥 " + YELLOW + "ONLY EAAD USER TOKENS SUPPORTED 💥" + RESET)
    print(RESET)

def menu():
    while True:
        show_logo()
        print(GREEN + "\n1️⃣  START LOADER")
        print("2️⃣  STOP LOADER")
        print("3️⃣  DISPLAY SENT MESSAGES")
        print("4️⃣  EXIT" + RESET)
        print("──────────────────────────────")
        choice = input("➤ Choose Option (1-4): ").strip()

        if choice == "1":
            start_loader()
        elif choice == "2":
            stop_loader()
        elif choice == "3":
            display_sms()
        elif choice == "4":
            print("\n👋 Exiting menu... (loader will still run in background!)")
            break
        else:
            print(RED + "\n❌ Invalid choice! Try again." + RESET)

        input("\n🔁 Press ENTER to return to menu...")

if __name__ == "__main__":
    menu()
