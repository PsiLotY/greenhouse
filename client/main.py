from time import sleep
import json
import config
from iotee import Iotee
import signal
import sys
import time 
from utils import connect_to_mqtt, subscribe_to, start_iotee

#handles shutting down threads on ctrl+c
def signal_handler(signal, frame, iotee):
    print('Shutting down')
    iotee.stop()
    sys.exit(0)
    
#define callback functions for mqtt
connflag = False
def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print('Connected with status: {0}'.format(response_code))

def on_publish(client, userdata, mid):
    print ('message number:', mid)

def on_message(client, userdata, msg):
    print("Message received, topic: ", msg.topic)
    print("Message payload: ", msg.payload.decode())


# message template
message = {
            "timestamp": 0,
            "inputName": "sensorData",
            "messageId": "555e8fef-6c80-48f3-a6b5-2d2160d472f5",
            "pressure": 0,
            "temperature": 0,
            "humidity": 0,
            "light": 0,
            "proximity": 0
            }

data = message


# callback functions for iotee
def on_temperature(value):
    data['temperature'] = value
    print("temperature: {:.2f}".format(value))


def on_humidity(value):
    data['humidity'] = value
    print("humidity: {:.2f}".format(value))


def on_light(value):
    data['light'] = value
    print("light: {:.2f}".format(value))


def on_proximity(value):
    data['proximity'] = value
    print("proximity: {:.2f}".format(value))



#gets the sensor data from the connected devive on COM_port through callback functions
def request_sensor_data(iotee):
    timestamp = int(time.time())
    print('\n')
    print('time of getting data:',timestamp)
    data['timestamp'] = timestamp
    iotee.request_temperature()
    iotee.request_humidity()
    iotee.request_light()
    iotee.request_proximity()



#main loop for sending data
def main():
    iotee = start_iotee(config.COM_port)
    signal.signal(signal.SIGINT, lambda signal, frame: signal_handler(signal, frame, iotee))

    iotee.on_temperature = on_temperature
    iotee.on_humidity = on_humidity
    iotee.on_light = on_light
    iotee.on_proximity = on_proximity


    client = connect_to_mqtt()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    subscribe_to(client, ['message_test'], 1)    
    while(True):
        request_sensor_data(iotee)
        
        sleep(1)
        client.publish('sensor_data', payload=json.dumps(data), qos=1)
        
        sleep(4)

if __name__ == '__main__':
    main()

