import unittest
import boto3
import dateutil
from unittest.mock import patch

from unittest.mock import MagicMock
from temperature_lambda import (
    query_database,
    format_temperature_data,
    get_device_ids,
    all_present_and_hot,
    temperature_handler
)

class TestMyModule(unittest.TestCase):
    def test_format_temperature_data(self):
        # Mock temperature response data
        temperature_response = {
            'Rows': [
                {'Data': [{'ScalarValue': 'temperature'}, {'ScalarValue': '2023-07-14'}, {'ScalarValue': '25.0'}, {'ScalarValue': '001'}]},
                {'Data': [{'ScalarValue': 'temperature'}, {'ScalarValue': '2023-07-14'}, {'ScalarValue': '26.0'}, {'ScalarValue': '002'}]}
            ]
        }

        # Call the function
        result = format_temperature_data(temperature_response)

        # Assertions
        expected_result = {
            0: {'measure_name': 'temperature', 'temperature': 25.0, 'device_id': '001', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': '002', 'timestamp': '2023-07-14'}
        }
        self.assertEqual(result, expected_result)

    def test_get_device_ids(self):
        # Mock query data
        query = {
            'Rows': [
                {'Data': [{'ScalarValue': '001'}]},
                {'Data': [{'ScalarValue': '002'}]}
            ]
        }

        # Call the function
        result = get_device_ids(query)

        # Assertions
        expected_result = ['001', '002']
        self.assertEqual(result, expected_result)
    
    def test_all_present_and_hot(self):
        # Mock temperature data and device IDs
        temperature_data = {
            0: {'measure_name': 'temperature', 'temperature': 25.0, 'device_id': 'device1', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': 'device2', 'timestamp': '2023-07-14'}
        }
        device_ids = ['device1', 'device2']

        # Call the function
        result = all_present_and_hot(temperature_data, device_ids)

        # Assertions
        self.assertFalse(result)

    def test_all_present_and_hot_not_present(self):
        # Mock temperature data and device IDs
        temperature_data = {
            0: {'measure_name': 'temperature', 'temperature': 25.0, 'device_id': 'device1', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': 'device2', 'timestamp': '2023-07-14'}
        }
        device_ids = ['device1', 'device2', 'device3']

        # Call the function
        result = all_present_and_hot(temperature_data, device_ids)

        # Assertions
        self.assertFalse(result)

    def test_all_present_and_hot_not_hot(self):
        # Mock temperature data and device IDs
        temperature_data = {
            0: {'measure_name': 'temperature', 'temperature': 20.0, 'device_id': 'device1', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': 'device2', 'timestamp': '2023-07-14'}
        }
        device_ids = ['device1', 'device2']

        # Call the function
        result = all_present_and_hot(temperature_data, device_ids)

        # Assertions
        self.assertFalse(result)
""" 
    @patch("temperature_handler.query_database")
    @patch("temperature_handler.get_device_ids")
    @patch("temperature_handler.format_temperature_data")
    @patch("temperature_handler.all_present_and_hot")
    @patch("temperature_handler.client.publish")
    def test_temperature_handler(self, mock_publish, mock_all_present_and_hot, mock_format_temperature_data, mock_get_device_ids, mock_query_database):
        # Mock the necessary dependencies and responses
        event = {"example_key": "example_value"}
        context = {}  # Provide an empty context or add relevant information if required
        device_query = "device_query"
        temperature_query = "temperature_query"
        device_response = "device_response"
        temperature_response = "temperature_response"
        temperature_data = "temperature_data"
        device_ids = ["device1", "device2"]

        mock_query_database.side_effect = [device_response, temperature_response]
        mock_get_device_ids.return_value = device_ids
        mock_format_temperature_data.return_value = temperature_data
        mock_all_present_and_hot.return_value = True
        mock_publish.return_value = {}

        # Call the function
        response = temperature_handler(event, context)

        # Assertions
        self.assertEqual(response, "opening windows")
        mock_query_database.assert_has_calls([
            unittest.mock.call(device_query),
            unittest.mock.call(temperature_query)
        ])
        mock_get_device_ids.assert_called_once_with(device_response)
        mock_format_temperature_data.assert_called_once_with(temperature_response)
        mock_all_present_and_hot.assert_called_once_with(temperature_data, device_ids)
        mock_publish.assert_called_once_with(
            topic='iot/sensor_data',
            qos=1,
            payload='{"open_windows": true}'
        )
 """
if __name__ == '__main__':
    unittest.main()