import json
import boto3
from botocore.exceptions import ClientError
import time
import datetime
from dateutil import tz

client = boto3.client('iot-data', region_name='eu-central-1')
timestream_client = boto3.client('timestream-query', region_name='eu-central-1')

def lambda_handler(event, context):
    message = event
    
    utc_time = datetime.datetime.utcnow()
    source_tz = tz.gettz('UTC')
    target_tz = tz.gettz('Europe/Berlin')
    
    current_time = utc_time.replace(tzinfo=source_tz).astimezone(target_tz).time()
    print(current_time)
    print(type(current_time))
    
    target_time = datetime.time(17, 0)
    print(target_time)
    
    query = 'Select timestamp, measure_name, measure_value::double from "sensorDataDB"."sensorDataTable" where measure_name=\'light\' and time>=DATE_TRUNC(\'day\', NOW())'
    response = timestream_client.query(QueryString=query)
    rows = response['Rows']
    
    light_exposure = 0
    if datetime.datetime.combine(datetime.date.today(), current_time) > datetime.datetime.combine(datetime.date.today(), target_time):
        for row in rows:
            timestamp = row['Data'][0]['ScalarValue']
            light_value = row['Data'][2]['ScalarValue']
            
            if int(float(light_value)) > 60:
                light_exposure += 5
                
        timestamp = int(time.time())
        message['timestamp'] = timestamp
        
        if light_exposure > 28800:
            message["need_light"] = False
            response = client.publish(
                topic='iot/sensor_data',
                qos=1,
                payload=json.dumps(message)
            )
            return 'nolight'
        else:
            message["need_light"] = True
            response = client.publish(
                topic='iot/sensor_data',
                qos=1,
                payload=json.dumps(message)
            )
            return 'needslight'
            
    return "not after 6"
