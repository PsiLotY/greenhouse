import json
import boto3
from datetime import datetime, time
from dateutil import tz

client = boto3.client('iot-data', region_name='eu-central-1')
timestream_client = boto3.client('timestream-query', region_name='eu-central-1')

def get_light_data():
    query = """
        WITH light_above_threshold AS (
            SELECT time, measure_value::double
            FROM sensorDataDB.sensorDataTable
            WHERE measure_name = 'light'
                AND time >= DATE_TRUNC('day', NOW())
        ),
        all_rows AS (
            SELECT measure_value::double, time,
                LEAD(time) OVER (ORDER BY time ASC) AS next_time,
                ROW_NUMBER() OVER (ORDER BY time ASC) AS row_number
            FROM light_above_threshold
        )
        SELECT measure_value::double, time, next_time
        FROM all_rows
        WHERE measure_value::double > 60
    """

    response = timestream_client.query(QueryString=query)
    return response

def get_sunlight_duration(response):
    rows = response['Rows']
    total_sunlight_duration = 0
    for row in rows:
        row_time = row['Data'][1]['ScalarValue'][:-3]
        next_time = row['Data'][2]['ScalarValue'][:-3] if 'ScalarValue' in row['Data'][2] else None
        
        row_time = datetime.strptime(row_time, '%Y-%m-%d %H:%M:%S.%f')
        next_time = datetime.strptime(next_time, '%Y-%m-%d %H:%M:%S.%f')
        
        duration = next_time - row_time
        duration = round(duration.total_seconds())
        
        total_sunlight_duration = total_sunlight_duration + duration
    return total_sunlight_duration

def evaluate_if_light(total_sunlight_duration, message):
    if total_sunlight_duration > 28800:
        print('enough sunlight')
        message["need_light"] = False
        response = client.publish(
            topic='iot/sensor_data',
            qos=1,
            payload=json.dumps(message)
        )
        return "doesn't need light"
    else:
        print('too little sunlight')
        message["need_light"] = True
        response = client.publish(
            topic='iot/sensor_data',
            qos=1,
            payload=json.dumps(message)
        )
        return 'needs light'

def lambda_handler(event, context):
    message = event
    
    utc_time = datetime.utcnow()
    source_tz = tz.gettz('UTC')
    target_tz = tz.gettz('Europe/Berlin')
    
    current_time = utc_time.replace(tzinfo=source_tz).astimezone(target_tz).time()
    target_time = time(17, 0)
    
    response = get_light_data()
    
    total_sunlight_duration = get_sunlight_duration(response)
        
    # the detector model only runs this lambda if current light < 60. 
    # thus no checks for that are needed
    if current_time > target_time:
        evaluate_if_light(total_sunlight_duration, message)
            
    return "not after 6"
