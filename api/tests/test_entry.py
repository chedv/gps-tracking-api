from django.test import TestCase

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK


class ApiEntryTest(TestCase):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.url = '/devices/{}/entries/'

    def post(self, device_id, entry_data):
        url = self.url.format(device_id)
        response = self.client.post(path=url, data=entry_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def get(self, device_id, entry_data):
        url = self.url.format(device_id)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('entries', response.data)
        self.assertIn(entry_data, response.data['entries'])
