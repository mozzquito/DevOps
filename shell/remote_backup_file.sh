#!/bin/bash

# กำหนดค่า
BACKUP_DIR="/home/itadmin/arda-cads-infra/dmc/Backup_postgres_data"
TODAY=$(date +"%d_%m_%Y")
FILE_PATTERN="backup_postgres_data_$TODAY.tar.gz"

REMOTE_USER="itadmin"
REMOTE_IP="xx.xx.xx.xx"
REMOTE_DIR="/home/itadmin/arda-database-backup/postgres_data"

# ส่งไฟล์ทั้งหมดที่ตรง pattern
for file in "$BACKUP_DIR"/$FILE_PATTERN; do
    echo "📤 กำลังส่ง: $file"
    scp "$file" "$REMOTE_USER@$REMOTE_IP:$REMOTE_DIR/"
done

# ลบไฟล์ที่เก่ากว่า 7 วันบนเครื่องปลายทาง (ผ่าน ssh)
ssh "$REMOTE_USER@$REMOTE_IP" "find $REMOTE_DIR -name '$FILE_PATTERN' -mtime +7 -exec rm -f {} \;"
