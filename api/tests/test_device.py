from django.test import TestCase

from rest_framework.status import HTTP_200_OK


class ApiDeviceTest(TestCase):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def get(self, device_data):
        response = self.client.get(path='/devices/', data=device_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('devices', response.data)
        self.assertIn(device_data, response.data['devices'])

    def put(self, device_data):
        response = self.client.put(path='/devices/', data=device_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
