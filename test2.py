import paho.mqtt.client as mqtt
import ssl, random
from time import sleep
import json
import config
from iotee import Iotee
import signal
import sys

def signal_handler(signal, frame):
    print('Shutting down')
    iotee.stop()
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

mqtt_url = config.mqtt_url
root_ca = config.root_ca
public_crt = config.public_crt  
private_key = config.private_key
COM_port = config.COM_port

connflag = False

def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print("Connected with status: {0}".format(response_code))

def on_publish(client, userdata, mid):
    print ('message number:', mid)


message = """{"messages": [{
                            "inputName": "test",
                            "messageId": "555e8fef-6c80-48f3-a6b5-2d2160d472f5",
                            "payload": {
                                "motorId": 1,
                                "sensorData": {
                                    "pressure": 0,
                                    "temperature": 0,
                                    "humidity": 0,
                                    "light": 0,
                                    "proximity": 0
                                }
                            },
                            "default": {
                                "motorId": 1,
                                "sensorData": {
                                    "pressure": 1,
                                    "temperature": 1,
                                    "humidity": 1,
                                    "light": 1,
                                    "proximity": 1
                                }
                            }
                            }
                        ]
                        }"""

data = json.loads(message)
print(data)

# iotee part
iotee = Iotee(COM_port)
iotee.start()

def on_temperature(value):
    data['messages'][0]['payload']['sensorData']['temperature'] = value
    print("temperature: {:.2f}".format(value))

def on_humidity(value):
    data['messages'][0]['payload']['sensorData']['humidity'] = value
    print("humidity: {:.2f}".format(value))

def on_light(value):
    data['messages'][0]['payload']['sensorData']['light'] = value
    print("light: {:.2f}".format(value))

def on_proximity(value):
    data['messages'][0]['payload']['sensorData']['proximity'] = value
    print("proximity: {:.2f}".format(value))

iotee.on_temperature = on_temperature
iotee.on_humidity = on_humidity
iotee.on_light = on_light
iotee.on_proximity = on_proximity

# mqtt connecting part
client = mqtt.Client()
client.tls_set(root_ca,
                certfile = public_crt,
                keyfile = private_key,
                cert_reqs = ssl.CERT_REQUIRED,
                tls_version = ssl.PROTOCOL_TLSv1_2,
                ciphers = None)
client.on_connect = on_connect
client.on_publish = on_publish

print ("Connecting to AWS IoT Broker...")
client.connect(mqtt_url, port = 8883, keepalive=60)
client.loop_start()

if __name__ == "__main__":
    while(True):
        # data = json.loads(message)
        print("Request")
        iotee.request_temperature()
        iotee.request_humidity()
        iotee.request_light()
        iotee.request_proximity()
        print("-----")
        sleep(1)
        if connflag == True:
            print ("Publishing...")
            print(data)
            client.publish("message_test", json.dumps(data), qos=1)
        else:
            client.connect(mqtt_url, port = 8883, keepalive=60)
            client.loop_start()
            print ("waiting for connection...")
        sleep(4)