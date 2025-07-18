import boto3
import schedule

ec2_client = boto3.client('ec2', region_name = 'eu-west-2')

volumes = ec2_client.describe_volumes(
    Filters=[     # filters out the production volumes
        {
            'Name': 'tag:Name' ,  # if tag key was env, write tag:env
            'Values': ['prod']   # list of values that you want to filter. e.g. could have been ['prod', 'staging']
        }

    ]
)
# print(volumes['Volumes'])

def creating_snapshot():
    for volume in volumes['Volumes']:
        volume_id = volume['VolumeId']
        response_snapshot = ec2_client.create_snapshot(
            VolumeId = volume_id
        )
        print(response_snapshot)


schedule.every(15).seconds.do(creating_snapshot)

while True:
    schedule.run_pending()