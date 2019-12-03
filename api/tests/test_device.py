from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED


class ApiDeviceTest(TestCase):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def get(self, data):
        response = self._send(APIClient.get, data, HTTP_200_OK)
        self.assertIn('devices', response)
        self.assertIn(data, response['devices'])
        return response

    def get_unauthorized(self, data):
        return self._send(APIClient.get, data, HTTP_401_UNAUTHORIZED)

    def put(self, data):
        return self._send(APIClient.put, data, HTTP_200_OK)

    def put_unauthorized(self, data):
        return self._send(APIClient.put, data, HTTP_401_UNAUTHORIZED)

    def _send(self, method, data, code):
        response = method(self.client, path='/devices/', data=data)
        self.assertEqual(response.status_code, code)
        return response.data
