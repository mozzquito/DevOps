import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('ecs', region_name="ap-southeast-1")

def lambda_handler(event, context):
    cluster = "cluster-preorder"
    service = "service-preinterest-manage-api"

    logger.info(f"Starting ECS service '{service}' in cluster '{cluster}'...")

    response = client.update_service(
        cluster=cluster,
        service=service,
        desiredCount=1  # ✅ "เปิด" โดยให้รัน 1 task
    )

    logger.info("Service started successfully.")
    logger.info(response)
