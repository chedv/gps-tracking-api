from django.test import TestCase

from rest_framework.status import (HTTP_201_CREATED, HTTP_200_OK,
                                   HTTP_401_UNAUTHORIZED)


class ApiEntryTest(TestCase):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def post(self, device_id, data, data_format=None):
        return self._post(device_id, data, data_format, HTTP_201_CREATED)

    def post_unauthorized(self, device_id, data, data_format=None):
        return self._post(device_id, data, data_format, HTTP_401_UNAUTHORIZED)

    def get(self, device_id, data, expected):
        response = self._get(device_id, data, HTTP_200_OK)
        self.assertIn(expected, response)
        return response

    def get_by_datetime(self, device_id, str_datetime, expected_list):
        data = dict(datetime=str_datetime)
        for expected in expected_list:
            self.get(device_id, data, expected)

    def get_by_type(self, device_id, accept_type, str_datetime, expected):
        data = {'accept-type': accept_type, 'datetime': str_datetime}
        response = self._get(device_id, data, HTTP_200_OK)
        self.assertEqual(expected, response)

    def get_unauthorized(self, device_id, data):
        return self._get(device_id, data, HTTP_401_UNAUTHORIZED)

    def _get(self, device_id, data, expected_code):
        url_data = [f'{key}={value}' for key, value in data.items()]
        url = f'/devices/{device_id}/entries?' + '&&'.join(url_data)
        response = self.client.get(path=url)
        self.assertEqual(expected_code, response.status_code)
        return response.data

    def _post(self, device_id, data, data_format, expected_code):
        url = f'/devices/{device_id}/entries'
        response = self.client.post(path=url, data=data, format=data_format)
        self.assertEqual(expected_code, response.status_code)
        return response.data
