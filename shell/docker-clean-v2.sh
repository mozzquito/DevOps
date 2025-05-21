#!/bin/bash

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"

send_to_gchat() {
  local message="$1"
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"text\": \"${message}\"}" "$WEBHOOK_URL"
}

send_to_gchat "เคลียร์ Docker prune: $(date)"
#delete  unused Docker images
docker image prune -a -f
send_to_gchat "ลบ unused Docker images เรียบร้อย"
#delete unused builder cache
docker builder prune -a -f
send_to_gchat "ลบ unused builder cache เรียบร้อย"
#delete dangling builder cache
docker builder prune -f
send_to_gchat "ลบ dangling builder cache เรียบร้อย"

send_to_gchat "เสร็จสิ้นทั้งหมด: $(date)"
