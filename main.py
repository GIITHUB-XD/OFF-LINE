import os
import threading
import time
import requests
import random
import string
import sqlite3
import json

os.makedirs("logs", exist_ok=True)

DB_FILE = "logs.db"

# SQLite Setup
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS message_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        convo_id TEXT,
        token TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

active_threads = {}

def generate_stop_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

def send_message(token, convo_id, message):
    url = f"https://graph.facebook.com/v19.0/t_{convo_id}/messages"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {"messaging_type": "MESSAGE_TAG", "tag": "CONFIRMED_EVENT_UPDATE", "message": {"text": message}}

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if "error" in data:
            if data['error']['code'] == 368:
                with open("blocked_tokens.txt", "a") as f:
                    f.write(token + "\n")
                print(f"⛔ Blocked Token Detected (code 368). Skipped.\n")
                return False
        else:
            cursor.execute("INSERT INTO message_logs (convo_id, token, message) VALUES (?, ?, ?)",
                           (convo_id, token, message))
            conn.commit()
            print(f"✅ Sent: {message}")
            return True
    except Exception as e:
        print(f"⚠️ Error: {e}")
    return False

def start_spam(tokens, convo_id, messages, delay, stop_key):
    def spam_thread():
        while True:
            if stop_key not in active_threads:
                break
            for token in tokens:
                message = random.choice(messages)
                if not send_message(token.strip(), convo_id, message.strip()):
                    continue
                time.sleep(delay)

    t = threading.Thread(target=spam_thread, daemon=True)
    active_threads[stop_key] = t
    t.start()

def stop_spam(stop_key):
    if stop_key in active_threads:
        del active_threads[stop_key]
        print("🛑 STOP LODER Activated. Thread stopped.")
    else:
        print("❌ STOP KEY Not Found.")

def show_messages(convo_id):
    cursor.execute("SELECT timestamp, message FROM message_logs WHERE convo_id = ?", (convo_id,))
    rows = cursor.fetchall()
    print(f"\n🧾 Messages sent to {convo_id}:")
    for row in rows:
        print(f"[{row[0]}] ➤ {row[1]}")
    print()

# UI
def main():
    while True:
        print("""
╔════════════════════════════════════╗
║       💬 FB CONVO TOOL (OFFLINE)   ║
╠════════════════════════════════════╣
║ 1. START LODER                     ║
║ 2. STOP LODER                      ║
║ 3. SHOW MESSAGE                    ║
║ 0. EXIT                            ║
╚════════════════════════════════════╝
""")
        choice = input("👉 Enter Option: ").strip()
        
        if choice == "1":
            tokens_file = input("📄 Enter Token File Name (e.g., tokens.txt): ").strip()
            convo_id = input("💬 Enter Convo ID: ").strip()
            hater_name = input("😡 Enter Hater Name: ").strip()
            message_file = input("📝 Enter Message File (e.g., messages.txt): ").strip()
            delay = float(input("⏱️ Enter Delay (in sec): ").strip())

            with open(tokens_file, "r") as tf:
                tokens = tf.readlines()

            with open(message_file, "r") as mf:
                messages = mf.readlines()

            stop_key = generate_stop_key()
            print(f"\n🟢 STARTED SPAMMER FOR '{hater_name}' WITH STOP KEY: {stop_key}\n")
            start_spam(tokens, convo_id, messages, delay, stop_key)

        elif choice == "2":
            stop_key = input("🛑 Enter STOP KEY to Stop: ").strip()
            stop_spam(stop_key)

        elif choice == "3":
            convo_id = input("🔍 Enter Convo ID to Show Messages: ").strip()
            show_messages(convo_id)

        elif choice == "0":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid Option. Try again.")

if __name__ == "__main__":
    main()
