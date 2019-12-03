from django.test import TestCase

from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK


class ApiUserTest(TestCase):
    def __init__(self, client, user_data):
        super().__init__()
        self.client = client
        self.user_data = user_data

    def register(self):
        response = self.client.post(path='/register/', data=self.user_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        return response.data

    def login(self):
        response = self.client.post(path='/login/', data=self.user_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('token', response.data)
        token_auth = 'Token {}'.format(response.data['token'])
        self.client.credentials(HTTP_AUTHORIZATION=token_auth)
        return response.data

    def logout(self):
        response = self.client.post(path='/logout/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        return response.data
