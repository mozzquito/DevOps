import boto3, json, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

REGION = 'ap-southeast-1'
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAQAolAlBVg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bvuLEOSf1xlCEjuOvJca13m-IYnR4gu4V_iw75zrLFw'
CPU_THRESHOLD = 80  # %

def lambda_handler(event, context):
    ecs = boto3.client('ecs', region_name=REGION)
    cw = boto3.client('cloudwatch', region_name=REGION)

    clusters = ecs.list_clusters()['clusterArns']
    if not clusters:
        return {'status': 'no clusters'}

    for cluster_arn in clusters:
        cluster_name = cluster_arn.split('/')[-1]
        service_arns = ecs.list_services(cluster=cluster_name)['serviceArns']
        if not service_arns:
            continue

        services = ecs.describe_services(cluster=cluster_name, services=service_arns)['services']

        for svc in services:
            svc_name = svc['serviceName']
            avg_cpu = get_cpu_utilization(cw, cluster_name, svc_name)

            if avg_cpu >= CPU_THRESHOLD:
                timestamp = now()
                msg = f"""
ECS CPU Alert%
Date: {timestamp}
Cluster: {cluster_name}
Service: {svc_name}
Average CPU: {avg_cpu:.2f}%"""
                send_to_chat(msg)

    return {'status': 'done'}

def get_cpu_utilization(cw, cluster, service):
    now_utc = datetime.utcnow()
    past = now_utc - timedelta(minutes=1)

    res = cw.get_metric_statistics(
        Namespace='AWS/ECS',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'ClusterName', 'Value': cluster},
            {'Name': 'ServiceName', 'Value': service}
        ],
        StartTime=past,
        EndTime=now_utc,
        Period=60,
        Statistics=['Average'],
        Unit='Percent'
    )

    data = res.get('Datapoints', [])
    return sorted(data, key=lambda x: x['Timestamp'])[-1]['Average'] if data else 0

def send_to_chat(message):
    req = urllib.request.Request(
        WEBHOOK,
        data=json.dumps({'text': message}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)

def now():
    return datetime.now(ZoneInfo("Asia/Bangkok")).strftime('%d-%m-%Y %H:%M:%S')
