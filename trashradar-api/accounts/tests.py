import json

from django.core.urlresolvers import reverse
from faker import Factory as FakerFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

faker = FakerFactory.create()


class RegisterUserTestCase(APITestCase):
    """
    Register a new user tests
    """
    api_version = 'v1'

    @property
    def account_list_view_name(self):
        return self.api_version + ':account-list'

    def test_create_without_permissions(self):
        """User creation successful without specifying permissions"""
        user_data = {
            'full_name': faker.name(),
            'email': faker.email(),
            'username': faker.email(),
            'phone': faker.phone_number(),
            'password': faker.password()
        }
        response = self.client.post(
            reverse(self.account_list_view_name),
            user_data,
        )
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'response from {} has 201 Created Status.'.format(
                             reverse(self.account_list_view_name)))

        token = Token.objects.get(user__username=user_data['username'])
        self.assertIn('token', stored_data, 'response does not contain the token.')
        self.assertNotIn('password', stored_data, 'response does not contain the password.')
        self.assertEqual(user_data['full_name'], stored_data['full_name'], 'Full name does not match')
        self.assertEqual(user_data['email'], stored_data['email'], 'Full name does not match')
        self.assertEqual(user_data['username'], stored_data['username'], 'Username does not match')
        self.assertEqual(user_data['phone'], stored_data['phone'], 'Phone does not match')
        self.assertEqual(token.key, stored_data['token'],
                         'token {} does not match with the stored on database {}.'.format(
                             token.key, stored_data['token']
                         ))
