#!/bin/bash

# ─── FOLDER SETUP ─────────────
SENT_LOG="sent_messages.txt"
RUNNING_DIR="running_tasks"
mkdir -p "$RUNNING_DIR"

# ─── COLORS ──────────────────
RED="\e[91m"
GREEN="\e[92m"
CYAN="\e[96m"
YELLOW="\e[93m"
RESET="\e[0m"

# ─── ANIMATED PRINT ──────────
type_print() {
  text="$1"
  for ((i = 0; i < ${#text}; i++)); do
    echo -ne "${text:$i:1}"
    sleep 0.01
  done
  echo ""
}

# ─── BROKEN NADEEM LOGO ──────
show_logo() {
  clear
  echo -e "${CYAN}"
  echo "██╗░░░██╗███████╗███╗░░██╗██████╗░███████╗███╗░░░███╗"
  echo "██║░░░██║██╔════╝████╗░██║██╔══██╗██╔════╝████╗░████║"
  echo "╚██╗░██╔╝█████╗░░██╔██╗██║██║░░██║█████╗░░██╔████╔██║"
  echo "░╚████╔╝░██╔══╝░░██║╚████║██║░░██║██╔══╝░░██║╚██╔╝██║"
  echo "░░╚██╔╝░░███████╗██║░╚███║██████╔╝███████╗██║░╚═╝░██║"
  echo -e "░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░░░░╚═╝${RESET}"
  echo -e "${YELLOW}               💥 LOADER TOOL BY BROKEN NADEEM 💥${RESET}\n"
}

# ─── KEY GENERATOR ───────────
generate_key() {
  RAND=$(head /dev/urandom | tr -dc A-Z0-9 | head -c 7)
  echo "BROKENNADEEM-$RAND"
}

# ─── START LOADER ────────────
start_loader() {
  echo -e "\n🔐 Enter path to TOKEN FILE:"
  read token_file
  [[ ! -f $token_file ]] && echo "❌ Token file not found!" && return

  echo -e "\n💬 Enter CONVERSATION UID:"
  read convo_id
  [[ -z $convo_id ]] && echo "❌ Invalid Convo ID!" && return

  echo -e "\n😡 Enter HATER NAME:"
  read hater_name

  echo -e "\n📁 Enter path to MESSAGE FILE:"
  read message_file
  [[ ! -f $message_file ]] && echo "❌ Message file not found!" && return

  echo -e "\n⏱️ Enter SPEED in seconds (e.g., 2):"
  read delay
  [[ -z $delay ]] && delay=2

  key=$(generate_key)
  task_file="$RUNNING_DIR/$key"
  touch "$task_file"

  (
    while IFS= read -r token; do
      while IFS= read -r message; do
        if [[ ! -f "$task_file" ]]; then
          echo "⛔ Task stopped: $key"
          exit
        fi

        curl -s -X POST "https://graph.facebook.com/v19.0/$convo_id/messages" \
          -d "recipient={\"thread_key\":\"$convo_id\"}" \
          -d "messaging_type=UPDATE" \
          -d "message={\"text\":\"$message\"}" \
          -d "access_token=$token" > /dev/null

        echo "$(date '+%Y-%m-%d %H:%M:%S') | $hater_name ➤ $message" >> "$SENT_LOG"
        sleep "$delay"
      done < "$message_file"
    done < "$token_file"
  ) &

  echo -e "\n${GREEN}✅ Loader started successfully!"
  echo -e "🆔 Your UNIQUE STOP KEY: ${YELLOW}$key${RESET}"
  echo -e "⚠️  Use this key in Option 2 to stop loader.\n"
}

# ─── STOP LOADER ─────────────
stop_loader() {
  echo -e "\n🔑 Enter your UNIQUE STOP KEY:"
  read stop_key
  rm -f "$RUNNING_DIR/$stop_key"
  echo -e "${RED}🛑 Requested stop for key: $stop_key${RESET}"
}

# ─── DISPLAY SENT MESSAGES ───
display_sms() {
  echo -e "\n📜 Sent Messages:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if [[ -f $SENT_LOG ]]; then
    cat "$SENT_LOG"
  else
    echo "📭 No messages sent yet."
  fi
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ─── MAIN MENU ───────────────
while true; do
  show_logo
  echo -e "${GREEN}1️⃣  START LOADER${RESET}"
  echo -e "${YELLOW}2️⃣  STOP LOADER${RESET}"
  echo -e "${CYAN}3️⃣  DISPLAY SENT MESSAGES${RESET}"
  echo -e "${RED}4️⃣  EXIT${RESET}"
  echo -ne "${CYAN}\n🔢 Choose Option (1-4): ${RESET}"
  read choice

  case $choice in
    1) start_loader ;;
    2) stop_loader ;;
    3) display_sms ;;
    4) echo -e "${RED}👋 Exiting..."; exit ;;
    *) echo -e "${RED}❌ Invalid input! Try 1-4.${RESET}" ;;
  esac

  echo -e "\n${YELLOW}⚡ Press ENTER to return to menu...${RESET}"
  read
done
