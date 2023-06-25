import json
from utils import connect_to_mqtt, subscribe_to, start_iotee
import config
import sys
import signal


#handles shutting down threads on ctrl+c
def signal_handler(signal, frame, iotee):
    print('Shutting down')
    iotee.stop()
    sys.exit(0)

#define callback functions for mqtt
def on_connect(client, userdata, flags, response_code):
    print('Connected with status: {0}'.format(response_code))

def on_subscribe(client, userdata, msg):
    print('Message received, topic: ', msg.topic)
    print(msg.payload)


def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode())
    if message['state'] == 'sprinklers_on':
        iotee.set_led(255, 0, 0) #red
        text = 'Sprinklers \nare on'
        display_text(text)
        print('Sprinklers are on')

    elif message['state'] == 'sprinklers_off':
        iotee.set_led(0, 255, 0) #green
        text = 'Sprinklers \nare off'
        display_text(text)
        print('Sprinklers are off')

    elif message['state'] == 'windows_closed':
        iotee.set_led(0, 0, 255) #blue
        text = 'Windows \nare closed'
        display_text(text)
        print('Windows are closed')

    elif message['state'] == 'windows_open':
        iotee.set_led(255, 255, 0) #yellow
        text = 'Windows \nare open'
        display_text(text)
        print('Windows are open')

    elif message['state'] == 'lights_on':
        iotee.set_led(0, 255, 255) #cyan
        text = 'Lights \nare on'
        display_text(text)
        print('Lights are on')

    elif message['state'] == 'lights_off':
        iotee.set_led(255, 0, 255) #purple
        text = 'Lights \nare off'
        display_text(text)
        print('Lights are off')


def process_text(text):
    global old_texts
    old_texts.append(text)
    # only keep the 3 newest appended texts if bigger than 3
    if len(old_texts) > 3:
        old_texts = old_texts[-3:]
    # create a new text of 3 elements from old_texts, seperated by \n
    new_text = ''
    for old_text in reversed(old_texts):
        new_text += f'{old_text}\n'
    return new_text

def display_text(text):
    text = process_text(text)
    iotee.set_display(text)

old_texts = []
iotee = start_iotee(config.COM_port)

#main loop for receiving data
def main():
    signal.signal(signal.SIGINT, lambda signal, frame: signal_handler(signal, frame, iotee))
    
    client = connect_to_mqtt()
    
    client.on_connect = on_connect
    client.on_message = on_message

    subscribe_to(client, ['iot/error', 'iot/actor_data'], 1)
    client.loop_forever()
    
    
if __name__ == '__main__':
    main()
