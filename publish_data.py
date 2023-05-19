import paho.mqtt.client as mqtt
import ssl, random
from time import sleep
import json
import config
from iotee import Iotee
import signal
import sys

#handles shutting down threads on ctrl+c
def signal_handler(signal, frame):
    print('Shutting down')
    iotee.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#gets data from config.py
mqtt_url = config.mqtt_url
root_ca = config.root_ca
public_crt = config.public_crt  
private_key = config.private_key
COM_port = config.COM_port

#define callback functions for mqtt
connflag = False
def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print('Connected with status: {0}'.format(response_code))

def on_publish(client, userdata, mid):
    print ('message number:', mid)
    
#setup mqtt client
client = mqtt.Client()
client.tls_set(root_ca,
                certfile = public_crt,
                keyfile = private_key,
                cert_reqs = ssl.CERT_REQUIRED,
                tls_version = ssl.PROTOCOL_TLSv1_2,
                ciphers = None)
client.on_connect = on_connect
client.on_publish = on_publish

#message template
message = """{"messages": [{
                            "inputName": "sensorData",
                            "messageId": "555e8fef-6c80-48f3-a6b5-2d2160d472f5",
                            "pressure": 0,
                            "temperature": 0,
                            "humidity": 0,
                            "light": 0,
                            "proximity": 0
                        }]
            }"""

data = json.loads(message)
print(data)

#setup iotee
iotee = Iotee(COM_port)
iotee.start()

#callback functions for iotee
def on_temperature(value):
    data['messages'][0]['temperature'] = value
    print('temperature: {:.2f}'.format(value))

def on_humidity(value):
    data['messages'][0]['humidity'] = value
    print('humidity: {:.2f}'.format(value))

def on_light(value):
    data['messages'][0]['light'] = value
    print('light: {:.2f}'.format(value))

def on_proximity(value):
    data['messages'][0]['proximity'] = value
    print('proximity: {:.2f}'.format(value))

iotee.on_temperature = on_temperature
iotee.on_humidity = on_humidity
iotee.on_light = on_light
iotee.on_proximity = on_proximity

#gets the sensor data from the connected devive on COM_port through callback functions
def request_sensor_data():
    iotee.request_temperature()
    iotee.request_humidity()
    iotee.request_light()
    iotee.request_proximity()
    print('\n')

#connect to AWS IoT core thing
print ('Connecting to AWS IoT Broker...')
client.connect(mqtt_url, port = 8883, keepalive=60)
client.loop_start()

#main loop for sending data
def main():
    while(True):
        request_sensor_data()
        
        sleep(1)
        if connflag == True:
            print ('Publishing...')
            print((data["messages"][0]["temperature"]))
            client.publish('message_test', json.dumps(data), qos=1)
        else:
            client.connect(mqtt_url, port = 8883, keepalive=60)
            client.loop_start()
            print ('waiting for connection...')
        sleep(4)




if __name__ == '__main__':
    main()