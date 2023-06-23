import unittest
from unittest.mock import MagicMock

from receiver import on_connect, on_subscribe, on_message

#TODO add assertions maybe
class TestReceiver(unittest.TestCase):

    def test_on_connect(self):
        client = MagicMock()
        userdata = MagicMock()
        flags = MagicMock()
        response_code = 0

        on_connect(client, userdata, flags, response_code)

    def test_on_subscribe(self):
        client = MagicMock()
        userdata = MagicMock()
        msg = MagicMock()

        on_subscribe(client, userdata, msg)

    def test_on_message(self):
        client = MagicMock()
        userdata = MagicMock()
        msg = MagicMock()

        on_message(client, userdata, msg)


if __name__ == '__main__':
    unittest.main()
