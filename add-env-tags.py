import boto3

ec2_client_ireland = boto3.client('ec2', region_name="eu-west-1") # ireland
ec2_resource_ireland = boto3.resource('ec2', region_name="eu-west-1")

reservations_ireland = ec2_client_ireland.describe_instances()['Reservations']

instance_ids_ireland = []  # list of Instance IDs that is currently empty, and filled as the for loop completes

for res in reservations_ireland:
    instances = res['Instances']
    for ins in instances:   # collect all instance IDs into a list
        instance_ids_ireland.append(ins['InstanceId']) # append the Instance IDs into the list created above one by one

response = ec2_resource_ireland.create_tags(
    Resources=instance_ids_ireland,
    Tags=[
        {
            'Key': 'env',
            'Value': 'prod'
        },
    ]
)


# Copy pasted the whole code for london below and changed variable names. And the tag is env:dev for london instances

ec2_client_london = boto3.client('ec2', region_name="eu-west-2")  # london
ec2_resource_london = boto3.resource('ec2', region_name="eu-west-2")

reservations_london = ec2_client_london.describe_instances()['Reservations']

instance_ids_london = []  # list of Instance IDs that is currently empty, and filled as the for loop completes

for res in reservations_london:
    instances = res['Instances']
    for ins in instances:  # collect all instance IDs into a list
        instance_ids_london.append(ins['InstanceId'])  # append the Instance IDs into the list created above one by one

response = ec2_resource_london.create_tags(
    Resources=instance_ids_london,
    Tags=[
        {
            'Key': 'env',
            'Value': 'dev'
        },
    ]
)


