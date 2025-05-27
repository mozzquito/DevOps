#!/bin/bash

REMOTE_USER="administrator"
REMOTE_IP="xx.xx.xx.xx"
TODAY=$(date +"%d_%m_%Y")

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw"

send_to_gchat() {
  local message="$1"
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"text\": \"$message\"}" "$WEBHOOK_URL"
}

STATUS=""
HOSTNAME=$(hostname)
TIME=$(TZ="Asia/Bangkok" date +"%d-%m-%Y %H:%M:%S")
PRIVATE_IP=$(hostname -I | awk '{print $1}')
PUBLIC_IP=$(wget -qO- http://checkip.amazonaws.com)

# ใช้ rsync ส่งไฟล์และลบไฟล์เก่าโดยตรงแบบไม่ใช้ loop
rsync -avz "/home/itadmin/arda-cads-infra/dmc/Backup_postgres_data/backup_postgres_data_$TODAY.tar.gz" \
  "$REMOTE_USER@$REMOTE_IP:/home/itadmin/arda-database-backup/postgres_data/"
STATUS+="Postgres data: rsync done\n"

rsync -avz "/home/itadmin/arda-cads-infra/dmc/Backup_extensions/backup_extensions_$TODAY.tar.gz" \
  "$REMOTE_USER@$REMOTE_IP:/home/itadmin/arda-database-backup/extensions/"
STATUS+="Extensions: rsync done\n"

rsync -avz "/home/itadmin/arda-cads-infra/minio/Backup_minio_storage/backup_minio_storage_$TODAY.tar.gz" \
  "$REMOTE_USER@$REMOTE_IP:/home/itadmin/arda-database-backup/minio_storage/"
STATUS+="Minio: rsync done\n"

# ลบไฟล์เก่ากว่า 7 วันจากเครื่องปลายทาง
ssh "$REMOTE_USER@$REMOTE_IP" "
  find /home/itadmin/arda-database-backup/postgres_data/ -name '*.tar.gz' -mtime +7 -delete
  find /home/itadmin/arda-database-backup/extensions/ -name '*.tar.gz' -mtime +7 -delete
  find /home/itadmin/arda-database-backup/minio_storage/ -name '*.tar.gz' -mtime +7 -delete
"

MESSAGE="*Transfer Backup to $REMOTE_IP*\nHost: $HOSTNAME\nIP: $PUBLIC_IP\nTime: $TIME\n\n$STATUS"
send_to_gchat "$MESSAGE"

echo -e "$MESSAGE"
