import iotee
from time import sleep
from threading import Thread

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

iotee.start()