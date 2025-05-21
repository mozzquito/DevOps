#!/bin/bash

# ตั้งค่าพาธ
BACKUP_SRC="/home/itadmin/arda-cads-infra/dmc/postgres_data"            
BACKUP_DST="/home/itadmin/arda-cads-infra/dmc/Backup_postgres_data"     
TODAY=$(date +"%d_%m_%Y")
FILENAME="backup_postgres_data_$TODAY.tar.gz"

# สร้างโฟลเดอร์ backup หากยังไม่มี
mkdir -p "$BACKUP_DST"

# สร้างไฟล์ backup (.tar.gz)
sudo tar -czf"$BACKUP_DST/$FILENAME" -C "$BACKUP_SRC" .

# ลบไฟล์ backup ที่เก่ากว่า 7 วัน
find "$BACKUP_DST" -name "backup-*.tar.gz" -mtime +7 -exec rm -f {} \;
