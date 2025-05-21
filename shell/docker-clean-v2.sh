#!/bin/bash
HOSTNAME=$(hostname)
DATETIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)
WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"

send_to_gchat() {
  local message="$1"
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"text\": \"${message}\"}" "$WEBHOOK_URL"
}

send_to_gchat "เคลียร์ Docker prune: $(date)"
#delete  unused Docker images
docker image prune -a -f
#delete unused builder cache
docker builder prune -a -f
#delete dangling builder cache
docker builder prune -f

MESSAGE="*Docker Clean Prune*\nTime: $DATETIME\nHost: $HOSTNAME\nIP: $PUBLIC_IP\n\n"
send_to_gchat "$MESSAGE"

