import json

from faker import Factory as FakerFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

faker = FakerFactory.create()


class RegisterUserTestCase(APITestCase):
    """
    Register a new user tests
    """
    def test_create_without_permissions(self):
        """User creation successful without specifying permissions"""
        data = {
            'full_name': faker.name(),
            'email': faker.email(),
            'username': faker.email(),
            'phone': faker.phone_number(),
            'password': faker.password()
        }
        response = self.client.post(
            '/api/v1/accounts',
            json.dumps(data),
            content_type='application/json'
        )
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'response from /api/1/users has 201 Created Status.')

        token = Token.objects.get(user__username=data['username'])
        self.assertIn('token', stored_data,
                      'response from /api/1/users does not contain the token.')
        self.assertNotIn('password', stored_data, 'response from /api/1/users does not contain the password.')
        self.assertEqual(data['full_name'], stored_data['full_name'], 'Full name does not match')
        self.assertEqual(data['email'], stored_data['email'], 'Full name does not match')
        self.assertEqual(data['username'], stored_data['username'], 'Username does not match')
        self.assertEqual(data['phone'], stored_data['phone'], 'Phone does not match')
        self.assertEqual(token.key, stored_data['token'],
                         'token {} from /api/1/users does not match with the stored on database {}.'.format(
                             token.key, stored_data['token']
                         ))
