#!/bin/bash

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQAolAlBVg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fPohB6wPu5BlnRVpEM81Nx4MdBDXSE3DWGqYF6K7m8g"

INSTANCE_NAME=$(hostname)
TIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
PRIVATE_IP=$(hostname -I | awk '{print $1}')
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)

CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk -F'id,' -v prefix="$prefix" '{split($1, vs, ","); v=vs[length(vs)]; sub("%", "", v); printf("%.0f\n", v)}')
CPU_USAGE=$((100 - CPU_IDLE))

THRESHOLD=80

if [ "$CPU_USAGE" -gt "$THRESHOLD" ]; then
    TEXT="Alarm CPUUtilization \nTime: $TIME\n Hostname: zoo-database-optimize \n IP: $PUBLIC_IP \n CPU: ${CPU_USAGE}%\n"
    curl -s -X POST -H 'Content-Type: application/json' -d "{\"text\": \"$TEXT\"}" "$WEBHOOK_URL" >/dev/null
fi
