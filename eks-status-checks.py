import boto3

client = boto3.client('eks', region_name="eu-west-1")

clusters = client.list_clusters()['clusters'] #cluster names


# fetch more information about the clusters now that we have their names

for cluster in clusters:
    response = client.describe_cluster(
        name=cluster
    )
    cluster_status = response['cluster']['status']
    print(f"Cluster {cluster} status is {cluster_status}")
    cluster_endpoint = response['cluster']['endpoint']
    print(f"Cluster {cluster}'s endpoint is {cluster_endpoint}")
    cluster_version = response['cluster']['version']
    print(f'Cluster version: {cluster_version}')
