import boto3, json, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

REGION = 'ap-southeast-1'
RDS_INSTANCES = ['igc-dev-database-instance-1']
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw'  # 🔁 ใส่ Webhook ของคุณ

def lambda_handler(event, context):
    rds = boto3.client('rds', region_name=REGION)

    for db_identifier in RDS_INSTANCES:
        try:
            res = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
            db = res['DBInstances'][0]
            status = db['DBInstanceStatus']
            endpoint = db.get('Endpoint', {}).get('Address', 'N/A')
            engine = db.get('Engine', 'N/A')
            time_th = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d-%m-%Y %H:%M:%S")

            msg = f"""Alarm RDS Status
Time: {time_th}
DB Identifier: {db_identifier}
Status: {status.upper()}
Engine: {engine}
Endpoint: {endpoint}"""

            send_to_chat(msg)

        except Exception as e:
            send_to_chat(f"❌ Error checking RDS {db_identifier}: {str(e)}")

    return {"status": "done"}

def send_to_chat(message):
    req = urllib.request.Request(
        WEBHOOK,
        data=json.dumps({'text': message}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
