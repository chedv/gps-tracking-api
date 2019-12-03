from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.status import (HTTP_201_CREATED, HTTP_200_OK,
                                   HTTP_401_UNAUTHORIZED)


class ApiEntryTest(TestCase):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def post(self, id, data):
        return self._send(APIClient.post, HTTP_201_CREATED, id, data)

    def post_unauthorized(self, id, data):
        return self._send(APIClient.post, HTTP_401_UNAUTHORIZED, id, data)

    def get(self, id, data, str_datetime=None):
        if str_datetime is None:
            send = {}
        else:
            send = {'datetime': str_datetime}
        response = self._send(APIClient.get, HTTP_200_OK, id, send)
        self.assertIn('entries', response)
        self.assertIn(data, response['entries'])
        return response

    def get_by_datetime(self, id, expected_list, str_datetime):
        for expected in expected_list:
            self.get(id, expected, str_datetime)

    def get_unauthorized(self, id, data):
        return self._send(APIClient.get, HTTP_401_UNAUTHORIZED, id, data)

    def _send(self, method, code, id, data):
        url = '/devices/{}/entries/'.format(id)
        response = method(self.client, path=url, data=data)
        self.assertEqual(response.status_code, code)
        return response.data
