#!/bin/bash

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"
HOSTNAME=$(hostname)
DATETIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)


# อ่าน Memory Info ใช้แค่ awk ไม่ใช้ grep
MEM_INFO=$(free -h | grep ^Mem: | awk '{print "Total: "$2" | Used: "$3" | Free: "$4" | Shared: "$5" | Buff/Cache: "$6" | Available: "$7}')

# อ่าน Buffer Memory ใช้ awk ตรง ๆ
get_buffer_memory() {
  awk '/^Buffers:/ {print int($2/1024)}' /proc/meminfo
}

send_gchat_message() {
  local message="$1"
  curl -s -X POST -H 'Content-Type: application/json' \
    -d "{\"text\": \"$message\"}" \
    "$WEBHOOK_URL" >/dev/null
}

BUFFER_BEFORE=$(get_buffer_memory)

# เคลียร์ memory
sync
echo 3 > /proc/sys/vm/drop_caches

BUFFER_AFTER=$(get_buffer_memory)

# เตรียมข้อความ
MESSAGE="*Buffer Memory Clear*\nTime: $DATETIME\nHost: $HOSTNAME\nIP: $PUBLIC_IP\n\n$MEM_INFO"

send_gchat_message "$MESSAGE"
