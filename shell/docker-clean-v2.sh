#!/bin/bash
HOSTNAME=$"bam-stack-test"
DATETIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)
WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"

send_to_gchat() {
  local message="$1"
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"text\": \"${message}\"}" "$WEBHOOK_URL"
}
send_to_gchat "เริ่มเคลียร์ Docker prune \n Host: $HOSTNAME \n Time: $DATETIME \n IP: $PUBLIC_IP"
#delete  unused Docker images
docker image prune -a -f
send_to_gchat "$HOSTNAME: docker image prune -a"
#delete unused builder cache
docker builder prune -a -f
send_to_gchat "$HOSTNAME: docker builder prune -a"
#delete dangling builder cache
docker builder prune -f
send_to_gchat "$HOSTNAME: docker builder prune"
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
send_to_gchat "$HOSTNAME: Clean Caches"

send_to_gchat "$HOSTNAME : Clean Docker prune and Clean Chaches "
