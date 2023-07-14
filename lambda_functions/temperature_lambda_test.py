import unittest
import boto3
import dateutil

from unittest.mock import MagicMock

try:
    from temperature_lambda import query_database, format_temperature_data, get_device_ids, all_present_and_hot, temperature_handler
except ModuleNotFoundError:
    from lambda_functions.temperature_lambda import query_database, format_temperature_data, get_device_ids, all_present_and_hot, temperature_handler

class TestMyModule(unittest.TestCase):
    def test_format_temperature_data(self):
        temperature_response = {
            'Rows': [
                {'Data': [{'ScalarValue': 'temperature'}, {'ScalarValue': '2023-07-14'}, {'ScalarValue': '25.0'}, {'ScalarValue': '001'}]},
                {'Data': [{'ScalarValue': 'temperature'}, {'ScalarValue': '2023-07-14'}, {'ScalarValue': '26.0'}, {'ScalarValue': '002'}]}
            ]
        }
        result = format_temperature_data(temperature_response)
        expected_result = {
            0: {'measure_name': 'temperature', 'temperature': 25.0, 'device_id': '001', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': '002', 'timestamp': '2023-07-14'}
        }
        self.assertEqual(result, expected_result)

    def test_get_device_ids(self):
        query = {
            'Rows': [
                {'Data': [{'ScalarValue': '001'}]},
                {'Data': [{'ScalarValue': '002'}]}
            ]
        }
        result = get_device_ids(query)
        expected_result = ['001', '002']
        self.assertEqual(result, expected_result)
    
    def test_all_present_and_hot(self):
        temperature_data = {
            0: {'measure_name': 'temperature', 'temperature': 25.0, 'device_id': 'device1', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': 'device2', 'timestamp': '2023-07-14'}
        }
        device_ids = ['device1', 'device2']
        result = all_present_and_hot(temperature_data, device_ids)
        self.assertFalse(result)

    def test_all_present_and_hot_not_present(self):
        temperature_data = {
            0: {'measure_name': 'temperature', 'temperature': 25.0, 'device_id': 'device1', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': 'device2', 'timestamp': '2023-07-14'}
        }
        device_ids = ['device1', 'device2', 'device3']
        result = all_present_and_hot(temperature_data, device_ids)
        self.assertFalse(result)

    def test_all_present_and_hot_not_hot(self):
        temperature_data = {
            0: {'measure_name': 'temperature', 'temperature': 20.0, 'device_id': 'device1', 'timestamp': '2023-07-14'},
            1: {'measure_name': 'temperature', 'temperature': 26.0, 'device_id': 'device2', 'timestamp': '2023-07-14'}
        }
        device_ids = ['device1', 'device2']
        result = all_present_and_hot(temperature_data, device_ids)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()