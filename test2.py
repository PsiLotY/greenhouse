import paho.mqtt.client as mqtt
import ssl, random
from time import sleep
import datetime
import json
import iotee
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

connflag = False

def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print("Connected with status: {0}".format(response_code))

def on_publish(client, userdata, mid):
    print (userdata, " -- ", mid)


message = """{"messages": [{
                            "inputName": "test",
                            "messageId": "555e8fef-6c80-48f3-a6b5-2d2160d472f5",
                            "payload": {
                                "motorId": 1,
                                "sensorData": {
                                    "pressure": 1,
                                    "temperature": 1
                                }
                            },
                            "default": {
                                "motorId": 1,
                                "sensorData": {
                                    "pressure": 1,
                                    "temperature": 1
                                }
                            }
                            }
                        ]
                        }"""
data = json.loads(message)
print(data['messages'][0]['payload']['sensorData']['temperature'])

# iotee part
iotee = iotee.Iotee("COM7")
iotee.start()
class MyIotee(Iotee):
    def on_temperature(self, value):
        data['messages'][0]['payload']['sensorData']['temperature'] = value
        print(data['messages'][0]['payload']['sensorData']['temperature'])
        print("temperature: {:.2f}".format(value))

    def on_humidity(self, value):
        print("humidity: {:.2f}".format(value))

    def on_light(self, value):
        print("light: {:.2f}".format(value))

    def on_proximity(self, value):
        print("proximity: {:.2f}".format(value))

if __name__ == "__main__":

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
            print(data['messages'][0]['payload']['sensorData']['temperature'])
            json.dumps(message)
            client.publish("message_test", message, qos=1)
            sleep(5)
        else:
            print ("waiting for connection...")