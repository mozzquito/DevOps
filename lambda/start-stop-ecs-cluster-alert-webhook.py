import boto3
import json
import urllib.request

client = boto3.client('ecs', region_name="ap-southeast-1")
WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAu5AVv2k/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=aL8LpOwD8P5EK2t8bPpHtqJq2umE6UElg6hOef4dUos"

def send_chat(text):
    data = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(WEBHOOK_URL, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

def lambda_handler(event, context):
    cluster = "spvi-prod-preorder"
    services = [
        "spvi-prod-preinterest-manage-api",
        "spvi-prod-preorder-admin",
        "spvi-prod-preorder-manage-api"
    ]

    messages = []
    for svc in services:
        try:
            client.update_service(cluster=cluster, service=svc, desiredCount=0)
            messages.append(f" ปิด {svc} สำเร็จ")
        except Exception as e:
            messages.append(f" ปิด {svc} ล้มเหลว\n→ {e}")

    send_chat("สถานะการปิด SPVI Pre Order\n" + "\n".join(messages))
