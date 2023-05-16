from iotee import Iotee
from time import sleep

        
iotee = Iotee("COM7")
iotee.start()

while(True):
    print("Request")
    iotee.request_temperature()
    iotee.request_humidity()
    iotee.request_light()
    iotee.request_proximity()
    print("-----")
    sleep(1)