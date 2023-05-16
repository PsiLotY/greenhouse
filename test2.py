import paho.mqtt.client as mqtt
import ssl, random
from time import sleep
import datetime
import json
import iotee
import config

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

iotee = iotee.Iotee("COM7")
iotee.start()
    
def connect_aws():
    client = mqtt.Client()
    client.tls_set(root_ca,
                   certfile = public_crt,
                   keyfile = private_key,
                   cert_reqs = ssl.CERT_REQUIRED,
                   tls_version = ssl.PROTOCOL_TLSv1_2,
                   ciphers = None)

if __name__ == "__main__":
    print ("Loaded MQTT configuration information.")    
    print ("Endpoint URL: " + mqtt_url)
    print ("Root Cert: " + root_ca)
    print ("Device Cert: " + public_crt)
    print ("Private Key: " + private_key)

    client = connect_aws()
    client.on_connect = on_connect
    client.on_publish = on_publish

    print ("Connecting to AWS IoT Broker...")
    client.connect(mqtt_url, port = 8883, keepalive=60)
    client.loop_start()
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

    while(True):
        print("Request")
        temperature = iotee.request_temperature()
        humidity = iotee.request_humidity()
        light = iotee.request_light()
        proximity = iotee.request_proximity()
        print("-----")
        sleep(1)
        if connflag == True:
            print ("Publishing...")
            data = json.loads(message)
            data['messages'][0]['payload']['sensorData']['pressure'] = 20
            data['messages'][0]['payload']['sensorData']['temperature'] = temperature
            json.dumps(message)
            client.publish("message_test", message, qos=1)
            sleep(5)
        else:
            print ("waiting for connection...")