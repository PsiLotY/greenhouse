from utils import connect_to_mqtt, subscribe_to


#define callback functions for mqtt
def on_connect(client, userdata, flags, response_code):
    print('Connected with status: {0}'.format(response_code))

def on_subscribe(client, userdata, msg):
    print("Message received, topic: ", msg.topic)
    print(msg.payload)

def on_message(client, userdata, msg):
    print("Message received, topic: ", msg.topic)
    print("Message payload: ", msg.payload.decode())

#main loop for receiving data
def main():
    client = connect_to_mqtt()
    
    client.on_connect = on_connect
    client.on_message = on_message

    subscribe_to(client, ['iot/debugging', 'iot/error', 'iot/actor_data'], 1)
    client.loop_forever()
    
    
if __name__ == '__main__':
    main()
