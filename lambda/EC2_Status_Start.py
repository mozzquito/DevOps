import boto3, json, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

INSTANCE_ID = 'i-065f1a8e566d2ccf7'
REGION = 'ap-southeast-1'
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/...'  # แก้เป็นของคุณ

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=REGION)
    i = ec2.describe_instances(InstanceIds=[INSTANCE_ID])['Reservations'][0]['Instances'][0]
    timestamp = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d-%m-%Y %H:%M:%S")


    if i['State']['Name'] == 'running':
        msg = f"""*EC2 Started*
            Name: {next((t['Value'] for t in i.get('Tags', []) if t['Key'] == 'Name'), 'Unknown')}
            ID: {INSTANCE_ID}
            IP: {i.get('PublicIpAddress', 'N/A')}
            Status: RUNNING
            Date: {timestamp}
        
        urllib.request.urlopen(urllib.request.Request(
            WEBHOOK,
            data=json.dumps({'text': msg}).encode(),
            headers={'Content-Type': 'application/json'}
        ))

    return {"status": i['State']['Name']}
