import paho.mqtt.client as mqtt
import ssl
from iotee import Iotee
import config

def connect_to_mqtt():
    '''Connects to a mqtt broker with tls encryption 
    
    Parameters: 
        None
        
    Returns: 
        client: mqtt client object
    '''
    mqtt_url = config.mqtt_url
    client = mqtt.Client()
    set_tls(client)
    print ('Connecting to AWS IoT Broker...')
    client.connect(mqtt_url, port = 8883, keepalive=120)
    return client

def set_tls(client: mqtt.Client):
    '''Sets the tls encryption for the mqtt client
    
    Parameters: 
        client: mqtt client object
        
    Returns: 
        None
    '''
    root_ca = config.root_ca
    public_crt = config.public_crt  
    private_key = config.private_key
    client.tls_set( root_ca,
                    certfile = public_crt,
                    keyfile = private_key,
                    cert_reqs = ssl.CERT_REQUIRED,
                    tls_version = ssl.PROTOCOL_TLSv1_2,
                    ciphers = None)
    

def subscribe_to(client: mqtt.Client, topics: list, qos: int):
    '''Subscribes to a list of topics 
    
    Parameters: 
        client (Client): mqtt client object
        topics (list): list of topics to subscribe to
        qos (int): quality of service
        
    Returns: 
        None
    '''
    for topic in topics:
        client.subscribe(topic, qos=qos)


def start_iotee(com_port: str):
    '''Starts a thread for the iotee device 
    
    Parameters: 
        com_port (str): com port where the iotee device is connected to
        
    Returns: 
        iotee: iotee object
    '''
    iotee = Iotee(com_port)
    iotee.start()
    return iotee