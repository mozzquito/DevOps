#!/bin/bash

THRESHOLD=1
HOSTNAME=$(hostname)
DATETIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQAolAlBVg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fPohB6wPu5BlnRVpEM81Nx4MdBDXSE3DWGqYF6K7m8g"
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)


send_gchat_message() {
  local message="$1"
  curl -s -X POST -H 'Content-Type: application/json' \
    -d "{\"text\": \"$message\"}" \
    "$WEBHOOK_URL" >/dev/null
}


df -P | awk -v threshold="$THRESHOLD" 'NR>1 {gsub("%","",$5); if ($5 >= threshold) printf "%s %.1fMB %.1fMB %d\n", $6, $3/1024, $2/1024, $5}' | while read -r PARTITION USED TOTAL USAGE; do
    MESSAGE="*Disk Alert*\nTime: $DATETIME\nHostname: zoo-database-optimize \n IP: $PUBLIC_IP\n Partition: $PARTITION\nStorage: $USED / $TOTAL (${USAGE}%)"
  send_gchat_message "$MESSAGE"
done
