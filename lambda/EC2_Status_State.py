import boto3, json, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

INSTANCE_ID = 'i-065f1a8e566d2ccf7'
REGION = 'ap-southeast-1'
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/...'  # แก้เป็นของคุณ

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=REGION)
    instance = ec2.describe_instances(InstanceIds=[INSTANCE_ID])['Reservations'][0]['Instances'][0]

    state = instance['State']['Name']
    name = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), 'Unknown')
    ip = instance.get('PublicIpAddress', 'N/A')
    time_th = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d-%m-%Y %H:%M:%S")

    msg = (
        f"*EC2 Instance Update*\n"
        f"Name: {name}\n"
        f"ID: {INSTANCE_ID}\n"
        f"IP: {ip}\n"
        f"Status: {state.upper()}\n"
        f"Time: {time_th}"
    )

    urllib.request.urlopen(urllib.request.Request(
        WEBHOOK,
        data=json.dumps({'text': msg}).encode(),
        headers={'Content-Type': 'application/json'}
    ))

    return {"status": state}
