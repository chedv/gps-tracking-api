from django.test import TestCase

from rest_framework.status import (HTTP_201_CREATED, HTTP_200_OK,
                                   HTTP_401_UNAUTHORIZED)


class ApiEntryTest(TestCase):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def post(self, device_id, data):
        return self._post(HTTP_201_CREATED, device_id, data)

    def post_unauthorized(self, device_id, data):
        return self._post(HTTP_401_UNAUTHORIZED, device_id, data)

    def get(self, device_id, params, expected):
        response = self._get(HTTP_200_OK, device_id, params)
        self.assertIn(expected, response)
        return response

    def get_by_datetime(self, device_id, str_datetime, expected_list):
        params = {'datetime': str_datetime}
        for expected in expected_list:
            self.get(device_id, params, expected)

    def get_by_type(self, device_id, export_type, str_datetime, expected):
        params = {'type': export_type, 'datetime': str_datetime}
        response = self._get(HTTP_200_OK, device_id, params)
        self.assertEqual(expected, response)

    def get_unauthorized(self, device_id, data):
        return self._get(HTTP_401_UNAUTHORIZED, device_id, data)

    def _get(self, expected_code, device_id, params):
        url_params = [f'{key}={value}' for key, value in params.items()]
        url = f'/devices/{device_id}/entries?' + '&&'.join(url_params)
        response = self.client.get(path=url)
        self.assertEqual(expected_code, response.status_code)
        return response.data

    def _post(self, expected_code, device_id, data):
        url = f'/devices/{device_id}/entries'
        response = self.client.post(path=url, data=data)
        self.assertEqual(expected_code, response.status_code)
        return response.data
