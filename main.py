import os
import time
import random
import string
import threading
import sys
import subprocess
import json

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

RUNNING_DIR = "running_tasks"
SENT_LOG = "sent_messages.txt"
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

def send_message(token, convo_id, message):
    import requests
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
                print(RED + "⚠️ Blocked Token Detected (code 368). Skipping token." + RESET)
                return False
            else:
                print(RED + f"⚠️ Error: {data['error'].get('message')}" + RESET)
                return False
        return True

    except Exception as e:
        print(RED + f"⚠️ Network error: {e}" + RESET)
        return False

def start_loader():
    keep_awake()
    print()
    animate_text(CYAN + "🔐 Enter path to TOKEN FILE:" + RESET)
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

    animate_text(CYAN + "⏱️ Enter SPEED in seconds (recommended: 5-10):" + RESET)  
    print("──────────────────────────────")  
    try:  
        speed = float(input("➤ ").strip())  
    except:  
        speed = 5.0

    key = generate_key()  
    task_file = os.path.join(RUNNING_DIR, key)  
    open(task_file, 'w').close()  

    def run_task():  
        while os.path.isfile(task_file):  
            with open(token_file, 'r') as tf:  
                tokens = [line.strip() for line in tf if line.strip()]  
            with open(message_file, 'r') as mf:  
                messages = [line.strip() for line in mf if line.strip()]  

            for token in tokens:  
                for msg in messages:  
                    if not os.path.isfile(task_file):  
                        print(RED + f"\n⛔ Task stopped: {key}" + RESET)  
                        return  
                    full_msg = f"@{hater_name} {msg}"  
                    success = send_message(token, convo_id, full_msg)
                    if success:
                        with open(SENT_LOG, 'a') as log:  
                            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {hater_name} ➤ {msg}\n")  
                        print(GREEN + f"✔ Sent: {msg}" + RESET)  
                    time.sleep(speed)

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
    print("   💥 " + YELLOW + "OFFLINE TOOL" + RESET + " BY BROKEN NADEEM 💥")
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
