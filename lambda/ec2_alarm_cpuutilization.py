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
    
    # ดึงข้อมูล CPU ปัจจุบัน (ย้อนหลัง 3 นาที)
    current_cpu = get_cpu_data(cloudwatch, minutes=3, period=60)
    
    # ดึงข้อมูล CPU เฉลี่ยย้อนหลัง 10 นาที
    avg_cpu = get_cpu_data(cloudwatch, minutes=10, period=300)
    
    # ดึงข้อมูล instance
    instance = ec2.describe_instances(InstanceIds=[INSTANCE_ID])['Reservations'][0]['Instances'][0]
    ip = instance.get('PublicIpAddress', 'ยังไม่มี IP')
    name = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), 'ไม่ระบุชื่อ')
    
    # สร้างข้อความ
    timestamp = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d-%m-%Y %H:%M:%S")
    msg = (
        f"Alarm CPUUtilization Over 80%\n"
        f"Date: {timestamp}\n"
        f"Hostname: {name}\n"
        f"IP: {ip}\n"
        f"Current CPU: {current_cpu:.2f}%\n"
        f"AVG CPU (10 min): {avg_cpu:.2f}%\n"
    )
    
    # ส่งข้อความ
    send_to_webhook(msg)
    
    return {"status": "ok", "current_cpu": current_cpu, "avg_cpu": avg_cpu}

def get_cpu_data(cloudwatch, minutes=5, period=300):
    """ดึงข้อมูล CPU จาก CloudWatch"""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)
    
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': INSTANCE_ID}],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average'],
        Unit='Percent'
    )
    
    datapoints = response.get('Datapoints', [])
    if not datapoints:
        return 0
    
    latest = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]
    return latest['Average']

def send_to_webhook(message):
    req = urllib.request.Request(
        WEBHOOK,
        data=json.dumps({"text": message}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
