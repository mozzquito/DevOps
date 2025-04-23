import json
import urllib.request


def lambda_handler(event, context):
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw'
    # ดึงข้อมูลจาก CloudWatch Event
    instance_id = event.get('detail', {}).get('instance-id', 'Unknown')
    region = event.get('region', 'Unknown')
    time = event.get('time', 'Unknown')

    message = (
f"""Instance Status Fail
Instance ID: `{instance_id}`
Time: `{time}`"""
    )

    data = json.dumps({'text': message}).encode('utf-8')
    
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    
    return {
        'statusCode': response.getcode(),
        'body': 'Notification sent'
    }
