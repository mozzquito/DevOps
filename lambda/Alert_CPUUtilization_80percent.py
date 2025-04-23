import boto3
import json
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ตั้งค่า
INSTANCE_ID = 'i-01fe12fd56c1de558'
REGION = 'ap-southeast-1'
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAQA2PdKSHc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=xZQeV8-BABJJYCvEk-Zcchzr68FCrZQuMJjsnmC_AoA'

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name=REGION)
    ec2 = boto3.client('ec2', region_name=REGION)

    # เวลาย้อนหลัง 10 นาที
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    # ดึงข้อมูล CPU จาก CloudWatch
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': INSTANCE_ID}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Percent'
    )

    datapoints = response.get('Datapoints', [])
    if not datapoints:
        msg = f'⚠️ ไม่พบข้อมูล CPU ของ Instance {INSTANCE_ID} ในช่วง 10 นาทีที่ผ่านมา'
        send_to_webhook(msg)
        return {"status": "no_data"}

    # ดึงค่าเฉลี่ยล่าสุด
    latest = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]
    avg_cpu = latest['Average']
    timestamp = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d-%m-%Y %H:%M:%S")

    # ดึงข้อมูล instance
    instance = ec2.describe_instances(InstanceIds=[INSTANCE_ID])['Reservations'][0]['Instances'][0]
    ip = instance.get('PublicIpAddress', 'ยังไม่มี IP')
    name = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), 'ไม่ระบุชื่อ')

    msg = (
        f"Alarm CPUUtilization Over 80%\n"
        f"Hostname: {name}\n"
        f"Instance ID: {INSTANCE_ID}\n"
        f"IP: {ip}\n"
        f"AVG CPU: {avg_cpu:.2f}%\n"
        f"Time: {timestamp}"
    )

    send_to_webhook(msg)

    return {"status": "reported", "cpu": avg_cpu, "ip": ip}


def send_to_webhook(message):
    req = urllib.request.Request(
        WEBHOOK,
        data=json.dumps({"text": message}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
