import json
import boto3

client = boto3.client('iot-data', region_name='eu-central-1')

def lambda_handler(event, context):
    print(event)
    temperature = event['messages'][0]['payload']['sensorData']['temperature']
    
    if temperature > 25:
        response = client.publish(
            topic='message_test',
            qos=1,
            payload=json.dumps({"temp":"high"})
        )
        print(response)
    else:
        response = client.publish(
            topic='message_test',
            qos=1,
            payload=json.dumps({"temp":"low"})
        )
        print(response)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Published to topic')
    }

