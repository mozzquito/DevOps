#!/bin/bash

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"

INSTANCE_NAME=$(hostname)
TIME=$(date '+%d-%m-%Y %H:%M:%S')
PRIVATE_IP=$(hostname -I | awk '{print $1}')
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk -F'id,' -v prefix="$prefix" '{split($1, vs, ","); v=vs[length(vs)]; sub("%", "", v); printf("%.0f\n", v)}')
CPU_USAGE=$((100 - CPU_IDLE))

THRESHOLD=80

if [ "$CPU_USAGE" -gt "$THRESHOLD" ]; then
    TEXT="🚨 CPU >80% | $INSTANCE_NAME ($PUBLIC_IP)\nTime: $TIME\nCPU: ${CPU_USAGE}%"
    curl -s -X POST -H 'Content-Type: application/json' -d "{\"text\": \"$TEXT\"}" "$WEBHOOK_URL" >/dev/null
fi
