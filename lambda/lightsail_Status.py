import json
import boto3
def lambda_handler(event, context):
    client = boto3.client('lightsail', region_name='ap-southeast-1')
    response = client.stop_instance(
    instanceName='Axebee-Security-Baseline-IMS'
)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
