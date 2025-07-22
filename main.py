import os
import time
import random
import string
import threading

RUNNING_DIR = "running_tasks"
SENT_LOG = "sent_messages.txt"
os.makedirs(RUNNING_DIR, exist_ok=True)

# 🔑 Generate Unique Key
def generate_key():
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return f"BROKENNADEEM-{rand}"

# ✅ START LOADER
def start_loader():
    token_file = input("\n🔐 Enter path to TOKEN FILE: ").strip()
    if not os.path.isfile(token_file):
        print("❌ Token file not found!")
        return

    convo_id = input("💬 Enter CONVERSATION UID: ").strip()
    if not convo_id:
        print("❌ Invalid Convo ID!")
        return

    hater_name = input("😡 Enter HATER NAME: ").strip()
    message_file = input("📁 Enter path to MESSAGE FILE: ").strip()
    if not os.path.isfile(message_file):
        print("❌ Message file not found!")
        return

    try:
        speed = float(input("⏱️ Enter SPEED in seconds (e.g., 2): ").strip())
    except:
        speed = 2.0

    key = generate_key()
    task_file = os.path.join(RUNNING_DIR, key)
    open(task_file, 'w').close()

    def run_task():
        with open(token_file, 'r') as tf:
            for token in tf:
                token = token.strip()
                with open(message_file, 'r') as mf:
                    for msg in mf:
                        msg = msg.strip()
                        if not os.path.isfile(task_file):
                            print(f"⛔ Task stopped: {key}")
                            return
                        cmd = (
                            f"curl -s -X POST https://graph.facebook.com/v19.0/{convo_id}/messages "
                            f"-d 'recipient={{\"thread_key\":\"{convo_id}\"}}' "
                            f"-d 'messaging_type=UPDATE' "
                            f"-d 'message={{\"text\":\"{msg}\"}}' "
                            f"-d 'access_token={token}' > /dev/null"
                        )
                        os.system(cmd)
                        with open(SENT_LOG, 'a') as log:
                            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {hater_name} ➤ {msg}\n")
                        time.sleep(speed)

    threading.Thread(target=run_task).start()
    print(f"\n✅ Loader Started Successfully!")
    print(f"🆔 Your UNIQUE STOP KEY: {key}")
    print("⚠️  Use Option 2 to stop using this key.\n")

# 🛑 STOP LOADER
def stop_loader():
    key = input("🔑 Enter your UNIQUE STOP KEY: ").strip()
    task_path = os.path.join(RUNNING_DIR, key)
    if os.path.isfile(task_path):
        os.remove(task_path)
        print(f"🛑 Requested to stop task with key: {key}")
    else:
        print("❌ Key not found or already stopped!")

# 📜 DISPLAY LOG
def display_sms():
    print("\n📜 Sent Messages Log:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if os.path.isfile(SENT_LOG):
        with open(SENT_LOG, 'r') as log:
            print(log.read())
    else:
        print("📭 No messages sent yet.")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# 🎨 Logo
def show_logo():
    os.system("clear")
    print("\033[96m")
    print("██╗░░░██╗███████╗███╗░░██╗██████╗░███████╗███╗░░░███╗")
    print("██║░░░██║██╔════╝████╗░██║██╔══██╗██╔════╝████╗░████║")
    print("╚██╗░██╔╝█████╗░░██╔██╗██║██║░░██║█████╗░░██╔████╔██║")
    print("░╚████╔╝░██╔══╝░░██║╚████║██║░░██║██╔══╝░░██║╚██╔╝██║")
    print("░░╚██╔╝░░███████╗██║░╚███║██████╔╝███████╗██║░╚═╝░██║")
    print("░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░░░░╚═╝")
    print("           💥 OFFLINE TOOL BY BROKEN NADEEM 💥")
    print("\033[0m")

# 🔁 MAIN MENU
def menu():
    while True:
        show_logo()
        print("1️⃣  START LOADER")
        print("2️⃣  STOP LOADER")
        print("3️⃣  DISPLAY SENT MESSAGES")
        print("4️⃣  EXIT")
        choice = input("\n🔢 Enter choice (1-4): ").strip()

        if choice == "1":
            start_loader()
        elif choice == "2":
            stop_loader()
        elif choice == "3":
            display_sms()
        elif choice == "4":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice!")

        input("\nPress ENTER to return to menu...")

# ▶️ Run
if __name__ == "__main__":
    menu()
