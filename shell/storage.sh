#!/bin/bash

# ค่าที่ตั้งไว้
THRESHOLD=80
HOSTNAME=$(hostname)
DATETIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQAolAlBVg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fPohB6wPu5BlnRVpEM81Nx4MdBDXSE3DWGqYF6K7m8g"
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)


# ฟังก์ชันส่งข้อความไปยัง Google Chat
send_gchat_message() {
  local message="$1"
  curl -s -X POST -H 'Content-Type: application/json' \
    -d "{\"text\": \"$message\"}" \
    "$WEBHOOK_URL" >/dev/null
}

# ตรวจสอบพื้นที่ดิสก์
df -P | awk -v threshold="$THRESHOLD" 'NR>1 {gsub("%","",$5); if ($5 >= threshold) print $6, $3, $2, $5}' | while read -r PARTITION USED TOTAL USAGE; do
  MESSAGE="*Disk Alert*\nTime: $DATETIME\nHost: $HOSTNAME\nIP: $PUBLIC_IP\nPartition: $PARTITION\nStorage: $USED / $TOTAL (${USAGE}%)"
  send_gchat_message "$MESSAGE"
done
