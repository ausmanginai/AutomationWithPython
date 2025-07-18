import boto3
from operator import itemgetter
ec2_client = boto3.client('ec2', region_name='eu-west-2')

volumes = ec2_client.describe_volumes(
    Filters=[     # filters out the production volumes
        {
            'Name': 'tag:Name' ,  # if tag key was env, write tag:env
            'Values': ['prod']   # list of values that you want to filter. e.g. could have been ['prod', 'staging']
        }

    ]
)

for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],  # only want snapshots created by my self
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )
    # we want to sort the list of dictionaries by the StartTime
    snapshots_sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)
    # snapshots['Snapshots] provides the actual list. Look at response syntax it will make sense
    # our snapshots list is now sorted by 'StartTime' values

    for snap in snapshots_sorted_by_date[2:]:  # [2:] means start the loop from the 3rd item (skip 0,1)
        ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )









