#!/bin/bash

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=xxxxxx"

send_to_gchat() {
  local message="$1"
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"text\": \"${message}\"}" "$WEBHOOK_URL"
}

TODAY=$(date +"%d_%m_%Y")
TIME=$(TZ='Asia/Bangkok' date '+%d-%m-%Y %H:%M:%S')
INSTANCE_NAME=$(hostname)
PRIVATE_IP=$(hostname -I | awk '{print $1}')
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)

STATUS=""

# Backup Minio
BACKUP_SRC="/home/itadmin/arda-cads-infra/minio/minio_storage"
BACKUP_DST="/home/itadmin/arda-cads-infra/minio/Backup_minio_storage"
FILENAME="backup_minio_storage_$TODAY.tar.gz"
mkdir -p "$BACKUP_DST"
sudo tar -czf "$BACKUP_DST/$FILENAME" -C "$BACKUP_SRC" .
STATUS+="backup minio done\n"

# Backup Extensions
BACKUP_SRC="/home/itadmin/arda-cads-infra/dmc/extensions"
BACKUP_DST="/home/itadmin/arda-cads-infra/dmc/Backup_extensions"
FILENAME="backup_extensions_$TODAY.tar.gz"
mkdir -p "$BACKUP_DST"
sudo tar -czf "$BACKUP_DST/$FILENAME" -C "$BACKUP_SRC" .
STATUS+="backup extension done\n"

# Backup Postgres Data
BACKUP_SRC="/home/itadmin/arda-cads-infra/dmc/postgres_data"
BACKUP_DST="/home/itadmin/arda-cads-infra/dmc/Backup_postgres_data"
FILENAME="backup_postgres_data_$TODAY.tar.gz"
mkdir -p "$BACKUP_DST"
sudo tar -czf "$BACKUP_DST/$FILENAME" -C "$BACKUP_SRC" .
STATUS+="backup postgres data done\n"

# Compose and Send Message
MESSAGE="*Backup Status Report*\nHost: $INSTANCE_NAME \nIP: $PUBLIC_IP\nTime: $TIME\n\n$STATUS"
send_to_gchat "$MESSAGE"

echo -e "$MESSAGE"
