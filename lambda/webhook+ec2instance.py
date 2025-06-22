import boto3, json, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

REGION = 'ap-southeast-1'
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAQA101hBdE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ynjaZw9nWJj2EJx6AWI84Rmx3svNwhD-dnsfk5NFVVw'
CPU_THRESHOLD = 1

# 👇 ใส่ EC2 instance ID ที่ต้องการตรวจสอบ
EC2_INSTANCE_IDS = ['i-0508930a5b5c6eb7b', 'i-0ebcbfba776a923e9']

def lambda_handler(event, context):
    ecs = boto3.client('ecs', region_name=REGION)
    cw = boto3.client('cloudwatch', region_name=REGION)

    # ✅ ECS Monitoring
    for cluster_arn in ecs.list_clusters().get('clusterArns', []):
        cluster_name = cluster_arn.split('/')[-1]
        services = ecs.list_services(cluster=cluster_name).get('serviceArns', [])
        if not services:
            continue

        for svc in ecs.describe_services(cluster=cluster_name, services=services)['services']:
            svc_name = svc['serviceName']
            avg_cpu = get_cpu_utilization(cw, 'AWS/ECS', [
                {'Name': 'ClusterName', 'Value': cluster_name},
                {'Name': 'ServiceName', 'Value': svc_name}
            ])
            if avg_cpu >= CPU_THRESHOLD:
                msg = f"""Alarm CPUUtilization 
Time: {now()}
Cluster: {cluster_name}
Service: {svc_name}
CPU: {avg_cpu:.2f}%"""
                send_to_chat(msg)

    # ✅ EC2 Monitoring
    for instance_id in EC2_INSTANCE_IDS:
        avg_cpu = get_cpu_utilization(cw, 'AWS/EC2', [
            {'Name': 'InstanceId', 'Value': instance_id}
        ])
        if avg_cpu >= CPU_THRESHOLD:
            send_alert_for_ec2(instance_id, avg_cpu)

    return {'status': 'done'}

def get_cpu_utilization(cw, namespace, dimensions):
    now_utc = datetime.utcnow()
    past = now_utc - timedelta(minutes=5)
    res = cw.get_metric_statistics(
        Namespace=namespace,
        MetricName='CPUUtilization',
        Dimensions=dimensions,
        StartTime=past,
        EndTime=now_utc,
        Period=300,
        Statistics=['Average'],
        Unit='Percent'
    )
    datapoints = res.get('Datapoints', [])
    return sorted(datapoints, key=lambda x: x['Timestamp'])[-1]['Average'] if datapoints else 0

def get_instance_details(instance_id):
    ec2 = boto3.client('ec2', region_name=REGION)
    reservations = ec2.describe_instances(InstanceIds=[instance_id]).get('Reservations', [])
    if not reservations:
        return ('Unknown', 'N/A')
    
    instance = reservations[0]['Instances'][0]
    hostname = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), instance_id)
    public_ip = instance.get('PublicIpAddress', 'N/A')
    return (hostname, public_ip)

def send_alert_for_ec2(instance_id, cpu):
    hostname, public_ip = get_instance_details(instance_id)
    time_str = now()
    msg = f"""Alarm CPUUtilization 
Time: {time_str}
Hostname: {hostname} 
IP: {public_ip} 
CPU: {cpu:.2f}%"""
    send_to_chat(msg)

def send_to_chat(message):
    req = urllib.request.Request(
        WEBHOOK,
        data=json.dumps({'text': message}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)

def now():
    return datetime.now(ZoneInfo("Asia/Bangkok")).strftime('%d-%m-%Y %H:%M:%S')
