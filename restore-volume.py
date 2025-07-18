import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name='eu-west-2')
ec2_resource = boto3.resource('ec2', region_name='eu-west-2')

instance_id = "i-070038028cab618a9" # hard-coded

volumes = ec2_client.describe_volumes(
    Filters=[
        {
        'Name': 'attachment.instance-id',
        'Values': [instance_id]
        }
    ]
)

#we know there is only one volume and we want to access that
instance_volume = volumes['Volumes'][0]

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],  # only want snapshots created by my self
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)

# sort the snapshots by latest on top, and [0] to insure we only get the latest
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot['StartTime'])

# create a new volume using the above latest snapshot
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="eu-west-2a", # harded-coded, although it could be fetched
    TagSpecifications=[  # assigning a tag as other scrips rely on this name:prod tag
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                }
            ]
        }
    ]
)

# make sure new volume is in 'Available' state before attaching to ec2-instance as otherwise you get an error
# it takes time for new volume to be in 'Available' state

while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    if vol.state == 'available':
        # attach the volume to the ec2-instance
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'  # made sure different directory to existing volume which is at /dev/xvda
        )
        break # break the loop once if function is performed





