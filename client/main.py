from time import sleep
import json
import config
from iotee import Iotee
import signal
import sys
import time
from utils import connect_to_mqtt, subscribe_to, start_iotee
import ssl

# handles shutting down threads on ctrl+c
def signal_handler(signal, frame, iotee):
    print('Shutting down')
    iotee.stop()
    sys.exit(0)


# define callback functions for mqtt
connflag = False


def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print('Connected with status: {0}'.format(response_code))


def on_publish(client, userdata, mid):
    print('message number:', mid)


def on_message(client, userdata, msg):
    print('Message received, topic: ', msg.topic)
    print('Message payload: ', msg.payload.decode())


# message template
message = {
    'timestamp': 0,
    'inputName': 'sensorData',
    'messageId': '555e8fef-6c80-48f3-a6b5-2d2160d472f5',
    'pressure': 0,
    'temperature': 0,
    'humidity': 0,
    'light': 0,
    'proximity': 0,
}
data = message


# callback functions for iotee
def on_temperature(value):
    data['temperature'] = value
    print('temperature: {:.2f}'.format(value))


def on_humidity(value):
    data['humidity'] = value
    print('humidity: {:.2f}'.format(value))


def on_light(value):
    data['light'] = value
    print('light: {:.2f}'.format(value))


def on_proximity(value):
    data['proximity'] = value
    print('proximity: {:.2f}'.format(value))


def on_button_pressed(value):
    global ran
    print('button pressed:', value)
    if value == 'A':
        data['temperature'] = 30  # >25
    elif value == 'B':
        data['temperature'] = 20  # <=25
    elif value == 'X':
        data['humidity'] = 10  # < 20
    elif value == 'Y':
        data['humidity'] = 30  # >= 20
    ran = True


# gets the sensor data from the connected devive on COM_port through callback functions
def request_sensor_data(iotee):
    timestamp = int(time.time())
    print('\n')
    print('time of getting data:', timestamp)
    data['timestamp'] = timestamp
    iotee.request_temperature()
    iotee.request_humidity()
    iotee.request_light()
    iotee.request_proximity()


ran = False
button_mode = False
# main loop for sending data
def main(button_mode):
    global ran
    iotee = start_iotee(config.COM_port)
    signal.signal(
        signal.SIGINT, lambda signal, frame: signal_handler(signal, frame, iotee)
    )

    iotee.on_temperature = on_temperature
    iotee.on_humidity = on_humidity
    iotee.on_light = on_light
    iotee.on_proximity = on_proximity
    iotee.on_button_pressed = on_button_pressed

    client = connect_to_mqtt()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    i = 0
    while True:
        try:
            if button_mode == False:
                request_sensor_data(iotee)
                print(data)
                sleep(1)
                client.publish('iot/sensor_data', payload=json.dumps(data), qos=1)
                sleep(4)
            else:
                if ran == True:
                    print(data)
                    client.publish('iot/sensor_data', payload=json.dumps(data), qos=1)
                    ran = False
                sleep(1)
        except ssl.SSLEOFError as e:
            print('SSL error occurred:', e)
            print('Attempting to reconnect')
            client.reconnect()
        except Exception as e:
            print('An error occurred:', e)


if __name__ == '__main__':
    main(button_mode=True)
