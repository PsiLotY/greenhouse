import paho.mqtt.client as mqtt
import ssl, random
from time import sleep
import datetime
import json
import iotee
from threading import Thread


mqtt_url = "a3uf1j30lr99lx-ats.iot.eu-central-1.amazonaws.com"
root_ca = 'aws_connect_test\\root-CA.crt'
public_crt = 'aws_connect_test\\Anjo_Laptop.cert.pem'
private_key = 'aws_connect_test\\Anjo_Laptop.private.key'

connflag = False

def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print("Connected with status: {0}".format(response_code))

def on_publish(client, userdata, mid):
    print (userdata + " -- " + mid)


if __name__ == "__main__":
    print ("Loaded MQTT configuration information.")    
    print ("Endpoint URL: " + mqtt_url)
    print ("Root Cert: " + root_ca)
    print ("Device Cert: " + public_crt)
    print ("Private Key: " + private_key)

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
#    client.loop_forever()
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
                        

    while True:
        sleep(0.5)
        print (connflag)
        if connflag == True:
            print ("Publishing...")
            ap_measurement = random.uniform(25.0, 150.0)
            timestamp = str(datetime.datetime.now())
            temp = random.uniform(20.0, 30.0)
            message = '{"timestamp":'+'"'+str(timestamp)+'",'+'"temperature":'+str(temp)+'}'
            
            data = json.loads(message)
            data['messages'][0]['payload']['motorId'] = 1   
            data['messages'][0]['payload']['sensorData']['pressure'] = 20
            data['messages'][0]['payload']['sensorData']['temperature'] = random.uniform(20.0, 30.0)
            print(data['messages'][0]['payload']['sensorData']['temperature'])  
            json.dumps(message)
            client.publish("message_test", message, qos=1)
            sleep(5)
        else:
            print ("waiting for connection...")




class Loop(Thread):
    def run(self):

        while(True):
            print("Request")
            iotee.request_temperature()
            iotee.request_humidity()
            iotee.request_light()
            iotee.request_proximity()
            print("-----")
            sleep(1)
iotee = iotee.Iotee("COM7")

loop = Loop()
 
loop.start()
