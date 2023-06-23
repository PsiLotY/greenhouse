import unittest
from unittest.mock import MagicMock
from config import COM_port
from utils import (
    connect_to_mqtt,
    set_tls,
    subscribe_to,
    start_iotee
)

#TODO add assertions maybe
class TestUtils(unittest.TestCase):

    def test_set_tls(self):
        client = MagicMock()
        
        set_tls(client)
    

    def test_subscribe_to(self):
        client = MagicMock()
        topics = ['topic1', 'topic2']
        qos = 1

        subscribe_to(client, topics, qos)


    def test_start_iotee(self):
        com_port = COM_port

        iotee = start_iotee(com_port)

        self.assertIsNotNone(iotee)


if __name__ == '__main__':
    unittest.main()
