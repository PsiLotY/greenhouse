import unittest
from unittest.mock import patch, MagicMock
import temperature_lambda


class TestTemperatureLambda(unittest.TestCase):
    @patch("boto3.client")
    def test_get_temperature_data(self, mock_client):
        mock_timestream = MagicMock()
        mock_client.return_value = mock_timestream
        expected_query = """
        SELECT t1.measure_name, t1.time, t1.measure_value::double AS temperature, t2.measure_value::varchar AS device_id
        FROM (
            SELECT measure_name, time, measure_value::double
            FROM sensor_data_db."sensor_data_table"
            WHERE measure_name = 'temperature'
            ORDER BY time DESC
            LIMIT 5
        ) AS t1
        JOIN (
            SELECT measure_name, time, measure_value::varchar
            FROM sensor_data_db."sensor_data_table"
            WHERE measure_name = 'device_id'
        ) AS t2 ON t1.time = t2.time
    """
        mock_timestream.query.return_value = "mocked response"

        actual_response = temperature_lambda.get_temperature_data()

        mock_timestream.query.assert_called_once_with(QueryString=expected_query)
        self.assertEqual(actual_response, "mocked response")

    @patch("boto3.client")
    def test_get_device_ids(self, mock_client):
        mock_timestream = MagicMock()
        mock_client.return_value = mock_timestream
        expected_query = """
        SELECT DISTINCT measure_value::varchar 
        FROM sensor_data_db."sensor_data_table" 
        WHERE measure_name='device_id'
    """
        mock_timestream.query.return_value = {
            "Rows": [
                {"Data": [{"ScalarValue": "device_1"}]},
                {"Data": [{"ScalarValue": "device_2"}]},
            ]
        }

        actual_device_ids = temperature_lambda.get_device_ids()

        mock_timestream.query.assert_called_once_with(QueryString=expected_query)
        self.assertEqual(actual_device_ids, ["device_1", "device_2"])

    @patch("boto3.client")
    def test_get_device_ids_exception(self, mock_client):
        mock_timestream = MagicMock()
        mock_client.return_value = mock_timestream
        mock_timestream.query.side_effect = Exception("An error occurred")

        with self.assertRaises(Exception) as context:
            temperature_lambda.get_device_ids()

        self.assertTrue('An error occurred' in str(context.exception))

    def test_format_temperature_data(self):
        mock_response = {
            "Rows": [
                {
                    "Data": [
                        {"ScalarValue": "temperature"},
                        {"ScalarValue": "1616161616"},
                        {"ScalarValue": "22.5"},
                        {"ScalarValue": "device_1"},
                    ]
                },
                {
                    "Data": [
                        {"ScalarValue": "temperature"},
                        {"ScalarValue": "1616162616"},
                        {"ScalarValue": "23.5"},
                        {"ScalarValue": "device_2"},
                    ]
                },
            ]
        }

        expected_result = {
            0: {
                "measure_name": "temperature",
                "temperature": 22.5,
                "device_id": "device_1",
                "timestamp": "1616161616",
            },
            1: {
                "measure_name": "temperature",
                "temperature": 23.5,
                "device_id": "device_2",
                "timestamp": "1616162616",
            },
        }

        actual_result = temperature_lambda.format_temperature_data(mock_response)
        self.assertEqual(actual_result, expected_result)

    def test_all_present_and_hot(self):
        temperature_data = {
            0: {
                "measure_name": "temperature",
                "temperature": 25.5,
                "device_id": "device_1",
                "timestamp": "1616161616",
            },
            1: {
                "measure_name": "temperature",
                "temperature": 24.5,
                "device_id": "device_2",
                "timestamp": "1616162616",
            },
            2: {
                "measure_name": "temperature",
                "temperature": 26.0,
                "device_id": "device_2",
                "timestamp": "1616163616",
            },
        }
        device_ids = ["device_1", "device_2"]

        actual_result = temperature_lambda.all_present_and_hot(
            temperature_data, device_ids
        )

        self.assertTrue(actual_result)

        temperature_data[2]["device_id"] = "device_3"
        actual_result = temperature_lambda.all_present_and_hot(
            temperature_data, device_ids
        )

        self.assertFalse(actual_result)

        temperature_data[1]["temperature"] = 24.0
        actual_result = temperature_lambda.all_present_and_hot(
            temperature_data, device_ids
        )

        self.assertFalse(actual_result)


if __name__ == "__main__":
    unittest.main()
