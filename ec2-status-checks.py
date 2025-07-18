import boto3
import schedule

ec2_client = boto3.client('ec2', region_name="eu-west-1")
ec2_resource = boto3.resource('ec2', region_name="eu-west-1")

def check_instance_status():
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True #to give details for terminated instances too
    )
    for status in statuses['InstanceStatuses']: # loops through individual instanceStatuses one by one
        ins_status = status['InstanceStatus']['Status'] # nested dictionary
        sys_status = status['SystemStatus']['Status']
        print(f" Instance {status['InstanceId']} status is {ins_status} and system status is {sys_status}")
        state = status['InstanceState']['Name'] #this was previously printed using describe_instance but this is quicker
        print(f" The instance state is {state}")
    print("#######\n")

# run the check_instance_status function every 5 minutes
schedule.every(5).seconds.do(check_instance_status) #syntax can be checked in the scheduler documentation

# This is to make the schedule task run all the time
while True:
    schedule.run_pending()



#reservations = ec2_client.describe_instances()   # this gives all the reservations (see response syntax)

#for reservation in reservations['Reservations']: #looping through the result for each individual reservation
#    instances = reservation['Instances'] # instances gives all the 'Instances' within that reservation
#    for instance in instances: #looping through the result for each instance in that particular reservation.
#        print(f" Status of instance {instance['InstanceId']} is {instance['State']['Name']}")
