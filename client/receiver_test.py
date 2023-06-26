import json
import unittest
from unittest.mock import Mock, patch
from receiver import on_message


class TestOnMessage(unittest.TestCase):
    def setUp(self):
        self.iotee_mock = Mock()
        self.client_mock = Mock()
        self.userdata_mock = Mock()
        self.msg_mock = Mock()

    def test_sprinklers_on(self):
        self.msg_mock.payload = json.dumps({"state": "sprinklers_on"}).encode()

        with patch("receiver.display_text") as display_text_mock:
            on_message(
                self.iotee_mock, self.client_mock, self.userdata_mock, self.msg_mock
            )

        self.iotee_mock.set_led.assert_called_with(255, 0, 0)
        display_text_mock.assert_called()

    def test_sprinklers_off(self):
        self.msg_mock.payload = json.dumps({"state": "sprinklers_off"}).encode()

        with patch("receiver.display_text") as display_text_mock:
            on_message(
                self.iotee_mock, self.client_mock, self.userdata_mock, self.msg_mock
            )

        self.iotee_mock.set_led.assert_called_with(0, 255, 0)
        display_text_mock.assert_called()

    def test_windows_closed(self):
        self.msg_mock.payload = json.dumps({"state": "windows_closed"}).encode()

        with patch("receiver.display_text") as display_text_mock:
            on_message(
                self.iotee_mock, self.client_mock, self.userdata_mock, self.msg_mock
            )

        self.iotee_mock.set_led.assert_called_with(0, 0, 255)
        display_text_mock.assert_called()

    def test_windows_open(self):
        self.msg_mock.payload = json.dumps({"state": "windows_open"}).encode()

        with patch("receiver.display_text") as display_text_mock:
            on_message(
                self.iotee_mock, self.client_mock, self.userdata_mock, self.msg_mock
            )

        self.iotee_mock.set_led.assert_called_with(255, 255, 0)
        display_text_mock.assert_called()

    def test_lights_on(self):
        self.msg_mock.payload = json.dumps({"state": "lights_on"}).encode()

        with patch("receiver.display_text") as display_text_mock:
            on_message(
                self.iotee_mock, self.client_mock, self.userdata_mock, self.msg_mock
            )

        self.iotee_mock.set_led.assert_called_with(0, 255, 255)
        display_text_mock.assert_called()

    def test_lights_off(self):
        self.msg_mock.payload = json.dumps({"state": "lights_off"}).encode()

        with patch("receiver.display_text") as display_text_mock:
            on_message(
                self.iotee_mock, self.client_mock, self.userdata_mock, self.msg_mock
            )

        self.iotee_mock.set_led.assert_called_with(255, 0, 255)
        display_text_mock.assert_called()


if __name__ == "__main__":
    unittest.main()
