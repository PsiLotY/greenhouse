import unittest
from unittest.mock import MagicMock, patch, call
from receiver import on_connect, on_message, on_subscribe, process_text


class TestReceiver(unittest.TestCase):
    @patch('builtins.print')
    def test_on_connect(self, mock_print):
        client = MagicMock()
        userdata = MagicMock()
        flags = MagicMock()
        response_code = 0

        on_connect(client, userdata, flags, response_code)

        mock_print.assert_called_once_with('Connected with status: 0')

    @patch('builtins.print')
    def test_on_subscribe(self, mock_print):
        client = MagicMock()
        userdata = MagicMock()
        msg = MagicMock()
        msg.topic = 'Test topic'

        on_subscribe(client, userdata, msg)

        calls = [call('Message received, topic: ', msg.topic), call(msg.payload)]
        mock_print.assert_has_calls(calls, any_order=True)

    @patch('builtins.print')
    def test_on_message(self, mock_print):
        client = MagicMock()
        userdata = MagicMock()
        msg = MagicMock()
        msg.topic = 'Test topic'
        msg.payload = b'Test payload'

        on_message(client, userdata, msg)

        calls = [
            call('Message received, topic: ', msg.topic),
            call('Message payload: ', '"Test payload"'),
        ]
        mock_print.assert_has_calls(calls, any_order=True)

    def test_process_text(self):
        text = 'Test text'
        processed_text = process_text(text)
        self.assertEqual(processed_text, 'Test text\n')
        
        text = 'Test text 2'
        processed_text = process_text(text)
        self.assertEqual(processed_text, 'Test text 2\nTest text\n')
        
        text = 'Test text 3'
        processed_text = process_text(text)
        self.assertEqual(processed_text, 'Test text 3\nTest text 2\nTest text\n')
        
        text = 'Test text 4'
        processed_text = process_text(text)
        self.assertEqual(processed_text, 'Test text 4\nTest text 3\nTest text 2\n')
        
    def display_text(self):
        pass


if __name__ == '__main__':
    unittest.main()
