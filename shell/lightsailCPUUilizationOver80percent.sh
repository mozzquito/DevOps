#!/bin/bash



WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"

INSTANCE_NAME=$(hostname)
TIME=$(date '+%d-%m-%Y %H:%M:%S')
IP=$(curl -s ifconfig.me)

CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}')
AVG_CPU=$(top -bn2 -d 0.5 | grep "Cpu(s)" | tail -n 1 | awk '{print 100 - $8}')

THRESHOLD=80

if (( $(echo "$CPU_USAGE > $THRESHOLD" | bc -l) )); then

   TEXT="Alarm CPUUtilization Over 80%\nServer:zoo-database-optimize\nDate: $TIME\nHostname: $INSTANCE_NAME\nIP: $IP\nCurrent CPU: ${CPU_USAGE}%\nAVG CPU (10 min): ${AVG_CPU}%"
        
   curl -X POST -H 'Content-Type: application/json' -d "{\"text\": \"$TEXT\"}" "$WEBHOOK_URL"
fi
