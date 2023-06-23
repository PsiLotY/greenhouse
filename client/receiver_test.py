import unittest
from unittest.mock import MagicMock, patch, call
from receiver import on_connect, on_message, on_subscribe


class TestReceiver(unittest.TestCase):
    @patch("builtins.print")
    def test_on_connect(self, mock_print):
        client = MagicMock()
        userdata = MagicMock()
        flags = MagicMock()
        response_code = 0

        on_connect(client, userdata, flags, response_code)

        mock_print.assert_called_once_with("Connected with status: 0")

    @patch("builtins.print")
    def test_on_subscribe(self, mock_print):
        client = MagicMock()
        userdata = MagicMock()
        msg = MagicMock()
        msg.topic = "Test topic"

        on_subscribe(client, userdata, msg)

        calls = [call("Message received, topic: ", msg.topic), call(msg.payload)]
        mock_print.assert_has_calls(calls, any_order=True)

    @patch("builtins.print")
    def test_on_message(self, mock_print):
        client = MagicMock()
        userdata = MagicMock()
        msg = MagicMock()
        msg.topic = "Test topic"
        msg.payload = b"Test payload"

        on_message(client, userdata, msg)

        calls = [
            call("Message received, topic: ", msg.topic),
            call("Message payload: ", '"Test payload"'),
        ]
        mock_print.assert_has_calls(calls, any_order=True)


if __name__ == "__main__":
    unittest.main()
