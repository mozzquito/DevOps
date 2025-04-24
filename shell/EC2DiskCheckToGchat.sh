#!/bin/bash

# ค่าที่ตั้งไว้
THRESHOLD=80
HOSTNAME=$(hostname)
DATETIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"

# ฟังก์ชันส่งข้อความไปยัง Google Chat
send_gchat_message() {
  local message="$1"
  curl -X POST -H 'Content-Type: application/json' \
    -d "{\"text\": \"$message\"}" \
    "$WEBHOOK_URL"
}
# ตรวจสอบพื้นที่ดิสก์
df -hP | grep -vE '^Filesystem|tmpfs|udev' | while read -r line; do
  USAGE=$(echo $line | awk '{print $5}' | sed 's/%//')
  USED=$(echo $line | awk '{print $3}')
  TOTAL=$(echo $line | awk '{print $2}')
  PARTITION=$(echo $line | awk '{print $6}')

  if [ "$USAGE" -ge "$THRESHOLD" ]; then
MESSAGE="*Alert Disk Storage Over 80%*
*Time:* $DATETIME
*Host:* $HOSTNAME
*Partition:* $PARTITION
*Storage:* $USED / $TOTAL (${USAGE}%)"
    send_gchat_message "$MESSAGE"
  fi
done
