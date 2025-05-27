#!/bin/bash

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=xxxxx

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


BACKUP_SRC="/home/itadmin/arda-cads-infra/minio/minio_storage"
BACKUP_DST="/home/itadmin/arda-cads-infra/minio/Backup_minio_storage"
FILENAME="backup_minio_storage_$TODAY.tar.gz"

mkdir -p "$BACKUP_DST"
if sudo tar -czf "$BACKUP_DST/$FILENAME" -C "$BACKUP_SRC" .; then
  find "$BACKUP_DST" -name "backup-*.tar.gz" -mtime +7 -exec rm -f {} \;
  STATUS+="backup minio pass\n"
else
  STATUS+="backup minio fail\n"
fi

BACKUP_SRC="/home/itadmin/arda-cads-infra/dmc/extensions"
BACKUP_DST="/home/itadmin/arda-cads-infra/dmc/Backup_extensions"
FILENAME="backup_extensions_$TODAY.tar.gz"

mkdir -p "$BACKUP_DST"
if sudo tar -czf "$BACKUP_DST/$FILENAME" -C "$BACKUP_SRC" .; then
  find "$BACKUP_DST" -name "backup-*.tar.gz" -mtime +7 -exec rm -f {} \;
  STATUS+="backup extension pass\n"
else
  STATUS+="backup extension fail\n"
fi

#3. Backup Postgres Data
BACKUP_SRC="/home/itadmin/arda-cads-infra/dmc/postgres_data"
BACKUP_DST="/home/itadmin/arda-cads-infra/dmc/Backup_postgres_data"
FILENAME="backup_postgres_data_$TODAY.tar.gz"

mkdir -p "$BACKUP_DST"
if sudo tar -czf "$BACKUP_DST/$FILENAME" -C "$BACKUP_SRC" .; then
  find "$BACKUP_DST" -name "backup-*.tar.gz" -mtime +7 -exec rm -f {} \;
  STATUS+="backup postgres data pass\n"
else
  STATUS+="backup postgres data fail\n"
fi

MESSAGE="*Backup Status Report*\nHost: $INSTANCE_NAME \nIP: $PUBLIC_IP\nTime: $TIME\n\n$STATUS"
send_to_gchat "$MESSAGE"

echo -e "$MESSAGE"
