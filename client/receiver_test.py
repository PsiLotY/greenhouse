import json
import unittest
from unittest.mock import Mock, patch
from receiver import process_text, on_message


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

    def test_process_text(self):
        text = "Test text"
        processed_text = process_text(text)
        self.assertEqual(processed_text, "Test text\n")

        text = "Test text 2"
        processed_text = process_text(text)
        self.assertEqual(processed_text, "Test text 2\nTest text\n")

        text = "Test text 3"
        processed_text = process_text(text)
        self.assertEqual(processed_text, "Test text 3\nTest text 2\nTest text\n")

        text = "Test text 4"
        processed_text = process_text(text)
        self.assertEqual(processed_text, "Test text 4\nTest text 3\nTest text 2\n")

    def display_text(self):
        pass


if __name__ == "__main__":
    unittest.main()
