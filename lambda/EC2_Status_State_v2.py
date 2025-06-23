import boto3, json, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

INSTANCE_IDS = [
    'i-0651fc0056fa2d678',
    'i-0aa5a5063f6e0e295',
    'i-03fdf0765e3b4db81',
    'i-0ee59f223ccd0e84c'
]
REGION = 'ap-southeast-1'
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw'

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=REGION)
    reservations = ec2.describe_instances(InstanceIds=INSTANCE_IDS)['Reservations']

    for res in reservations:
        for instance in res['Instances']:
            state = instance['State']['Name']
            instance_id = instance['InstanceId']
            name = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), instance_id)
            ip = instance.get('PublicIpAddress', 'N/A')
            time_th = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d-%m-%Y %H:%M:%S")

            msg = (
                f"Alarm EC2 Status\n"
                f"Time: {time_th}\n"
                f"Hostname: {name}\n"
                f"IP: {ip}\n"
                f"Status: {state.upper()}"
            )

            urllib.request.urlopen(urllib.request.Request(
                WEBHOOK,
                data=json.dumps({'text': msg}).encode(),
                headers={'Content-Type': 'application/json'}
            ))

    return {"status": "done"}
