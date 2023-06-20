import paho.mqtt.client as mqtt
from time import sleep
import config
import ssl

#gets data from config.py
mqtt_url = config.mqtt_url
root_ca = config.root_ca
public_crt = config.public_crt  
private_key = config.private_key

#define callback functions for mqtt
connflag = False
def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print('Connected with status: {0}'.format(response_code))

def on_subscribe(client,userdata, msg):
    print("Message received, topic: ", msg.topic)
    print(msg.payload)

def on_message(client, userdata, msg):
    print("Message received, topic: ", msg.topic)
    print("Message payload: ", msg.payload.decode())

#setup mqtt client
client = mqtt.Client()
client.tls_set(root_ca,
                certfile = public_crt,
                keyfile = private_key,
                cert_reqs = ssl.CERT_REQUIRED,
                tls_version = ssl.PROTOCOL_TLSv1_2,
                ciphers = None)

client.on_connect = on_connect
client.on_message = on_message


#main loop for receiving data
def main():
    client.connect(mqtt_url, port = 8883, keepalive=60)
    client.subscribe('status', qos=1)
    client.subscribe('error', qos=1)
    client.loop_forever()
    
    
if __name__ == '__main__':
    main()
