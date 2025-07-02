# WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAu5AVv2k/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=aL8LpOwD8P5EK2t8bPpHtqJq2umE6UElg6hOef4dUos"
#WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQA6_veoI0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=1SN4Z_v_PJLSBaIha4hd9mkrqyQhqx60BBB9_l9qQBQ"

import boto3
import json
import urllib.request

# สร้าง client ECS
ecs = boto3.client('ecs', region_name="ap-southeast-1")

# URL ของ Google Chat Webhook
WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQA6_veoI0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=1SN4Z_v_PJLSBaIha4hd9mkrqyQhqx60BBB9_l9qQBQ"

def send_chat(text):
    try:
        data = json.dumps({"text": text}).encode("utf-8")
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as res:
            print(f"✅ Google Chat Notified, Status: {res.status}")
    except Exception as e:
        print(f"❌ Error sending message to Google Chat: {e}")

def lambda_handler(event, context):
    # รับค่าจาก event หรือใช้ค่าดีฟอลต์
    cluster = event.get("cluster", "itc-prod-ecom")
    services = event.get("services", ["itc-prod-pim","itc-prod-pagerendering","itc-prod-inventory","itc-prod-cart","itc-prod-website"])
    desired_count = int(event.get("desiredCount",1))

    messages = [f"📉 เพิ่มจำนวน Task ของ ECS Services ใน Cluster `{cluster}` เหลือ `{desired_count}`"]

    for service in services:
        try:
            ecs.update_service(
                cluster=cluster,
                service=service,
                desiredCount=desired_count
            )
            messages.append(f"✅ {service} ลดสำเร็จ")
        except Exception as e:
            messages.append(f"❌ {service} ล้มเหลว\n→ {str(e)}")

    # ส่งข้อความเข้า Google Chat
    send_chat("\n".join(messages))

    return {
        'statusCode': 200,
        'body': 'Done'
    }
