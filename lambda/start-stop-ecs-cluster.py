import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('ecs', region_name="ap-southeast-1")

def lambda_handler(event, context):
    cluster = "cluster-prod-preorder"
    services = [
        "ecs-cluster-1",
        "ecs-cluster-2",
        "ecs-cluster-3"
    ]

    for service in services:
        try:
            logger.info(f"Starting ECS service '{service}' in cluster '{cluster}'...")
            response = client.update_service(
                cluster=cluster,
                service=service,
                desiredCount=1 # เปิด กี่ tack
                #desiredCount=0 # ปิด tack
            )
            logger.info(f"✅ Service '{service}' started.")
        except Exception as e:
            logger.error(f"❌ Failed to start service '{service}': {str(e)}")
