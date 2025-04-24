#!/bin/bash

# ตั้งค่า
WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/xxx/messages?key=xxx&token=xxx"
INSTANCE_NAME=$(hostname)
TIME=$(date '+%d-%m-%Y %H:%M:%S')
IP=$(curl -s ifconfig.me)

# ดึงค่า CPU
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
AVG_CPU=$(top -bn2 -d 0.5 | grep "Cpu(s)" | tail -n 1 | awk '{print 100 - $8}')

# กำหนด Threshold
THRESHOLD=80

# ตรวจสอบ
if (( $(echo "$CPU_USAGE > $THRESHOLD" | bc -l) )); then
    TEXT="Alarm CPUUtilization Over 80%\nDate: $TIME\nHostname: $INSTANCE_NAME\nIP: $IP\nCurrent CPU: ${CPU_USAGE}%\nAVG CPU (10 min): ${AVG_CPU}%"
    
    curl -X POST -H 'Content-Type: application/json' -d "{\"text\": \"$TEXT\"}" "$WEBHOOK_URL"
fi
