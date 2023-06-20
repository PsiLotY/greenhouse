import unittest
from unittest import mock
from unittest.mock import patch
import json
import boto3

from temp_lambda import lambda_handler


class TestLambdaFunction(unittest.TestCase):
    @mock.patch("boto3.client")
    def test_lambda_handler_high_temp(self, mock_boto_client):
        mock_response = {"statusCode": 200, "body": json.dumps("Published to topic")}
        mock_boto_client.return_value.publish.return_value = mock_response

        event = {"temperature": 30}
        context = {}

        response = lambda_handler(event, context)

        mock_boto_client.assert_called_once_with("iot-data", region_name="eu-central-1")
        mock_boto_client.return_value.publish.assert_called_once_with(
            topic="message_test", qos=1, payload=json.dumps({"temp": "high"})
        )

        self.assertEqual(response, mock_response)

    @mock.patch("boto3.client")
    def test_lambda_handler_low_temp(self, mock_boto_client):
        mock_response = {"statusCode": 200, "body": json.dumps("Published to topic")}
        mock_boto_client.return_value.publish.return_value = mock_response

        event = {"temperature": 20}
        context = {}

        response = lambda_handler(event, context)

        mock_boto_client.assert_called_once_with("iot-data", region_name="eu-central-1")
        mock_boto_client.return_value.publish.assert_called_once_with(
            topic="message_test", qos=1, payload=json.dumps({"temp": "low"})
        )

        self.assertEqual(response, mock_response)


if __name__ == "__main__":
    unittest.main()
