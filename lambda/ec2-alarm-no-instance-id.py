import boto3
import json
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

REGION = 'ap-southeast-1'
WEBHOOK = 'xxx'  # แก้ไขให้ตรงของคุณ

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=REGION)
    cloudwatch = boto3.client('cloudwatch', region_name=REGION)

    # ดึง instance ทั้งหมดที่กำลังรัน
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            name = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), 'Unnamed')
            ip = instance.get('PublicIpAddress', 'No IP')

            # ดึง CPU 5 นาทีล่าสุด
            now = datetime.utcnow()
            metric = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=now - timedelta(minutes=5),
                EndTime=now,
                Period=300,
                Statistics=['Average']
            )

            cpu = metric['Datapoints'][0]['Average'] if metric['Datapoints'] else 0
            time = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d-%m-%Y %H:%M:%S")

            # แจ้งเตือนเมื่อ CPU > 80%
            if cpu > 10:
                msg = f"Alarm TAT-ORG CPU Over \nTime: {time}\nHostname: {name}\n{ip}\nInstance ID: {instance_id}\nCPU: {cpu:.1f}%"
                send_to_google_chat(msg)

    return {"status": "done"}

def send_to_google_chat(message):
    req = urllib.request.Request(
        WEBHOOK,
        data=json.dumps({"text": message}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
