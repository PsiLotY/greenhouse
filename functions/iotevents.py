import boto3

def create_detector_model(event, context):
    client = boto3.client('iotevents')

    response = client.create_detector_model(
        detectorModelName = event['detectorModelName'],
        detectorModelDefinition = event['detectorModelDefinition'],
        roleArn = event['roleArn']
    )

