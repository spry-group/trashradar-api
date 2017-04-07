import json

from faker import Factory as FakerFactory
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account
from complaints.models import Complaint, Entity

faker = FakerFactory.create()


class ComplaintsTestCase(APITestCase):

    fixtures = ['complaints', 'entities', 'accounts']

    def test_list_entities_unauthenticated(self):
        """Fetch all the complaints"""
        response = self.client.get('/api/v1/complaints')
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response from /api/1/complaints has 200 Ok.')

        returned_complaint = stored_data['results'][0]
        self.assertIn('id', returned_complaint, 'Id is not present on the result data')
        complaint = Complaint.objects.get(pk=returned_complaint['id'])

        self.assertEqual(complaint.counter, returned_complaint['counter'], 'Name does not match')


class EntitiesTestCase(APITestCase):
    """
    Entities tests
    """
    fixtures = ['entities', 'accounts']

    def setUp(self):
        self.entity = {
            'name': 'New name',
            'twitter': 'newAccount',
            'phone': '987-654321',
            'template_message': 'New message'
        }

    def test_list_entities_unauthenticated(self):
        """Fetch all the entities"""
        response = self.client.get('/api/v1/entities')
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response from /api/1/entities has 200 Ok.')

        returned_entity = stored_data['results'][0]
        self.assertIn('id', returned_entity, 'Id is not present on the result data')
        entity = Entity.objects.get(pk=returned_entity['id'])

        self.assertEqual(entity.name, returned_entity['name'], 'Name does not match')
        self.assertEqual(entity.twitter, returned_entity['twitter'], 'Twitter does not match')
        self.assertEqual(entity.phone, returned_entity['phone'], 'Phone does not match')
        self.assertNotIn('template_message', returned_entity, 'Message is present on the result data')

    def test_get_entity_unauthenticated(self):
        """Fetch specific entity"""
        entity = Entity.objects.first()
        response = self.client.get('/api/v1/entities/{}'.format(entity.pk))
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response from /api/1/entities has 200 Ok.')

        self.assertEqual(entity.name, stored_data['name'], 'Name does not match')
        self.assertEqual(entity.twitter, stored_data['twitter'], 'Twitter does not match')
        self.assertEqual(entity.phone, stored_data['phone'], 'Phone does not match')
        self.assertNotIn('template_message', stored_data, 'Message is present on the result data')

    def test_create_entity_unauthenticated(self):
        """Trying to create an entity being unauthenticated"""
        response = self.client.post(
            '/api/v1/entities',
            json.dumps(self.entity),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from /api/1/entities has 401 Unauthorized.')

    def test_create_entity_authenticated(self):
        """Trying to create an entity being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        response = self.client.post(
            '/api/v1/entities',
            json.dumps(self.entity),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         'response from /api/1/entities has 403 Forbidden.')

    def test_update_entity_unauthenticated(self):
        """Trying to update an entity being unauthenticated"""
        entity = Entity.objects.first()
        response = self.client.put(
            '/api/v1/entities/{}'.format(entity.pk),
            json.dumps(self.entity),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from /api/1/entities has 401 Unauthorized.')

    def test_update_entity_authenticated(self):
        """Trying to update an entity being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        entity = Entity.objects.first()
        response = self.client.put(
            '/api/v1/entities/{}'.format(entity.pk),
            json.dumps(self.entity),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         'response from /api/1/entities has 403 Forbidden.')

    def test_delete_entity_unauthenticated(self):
        """Trying to delete an entity being unauthenticated"""
        entity = Entity.objects.first()
        response = self.client.delete('/api/v1/entities/{}'.format(entity.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from /api/1/entities has 401 Unauthorized.')

    def test_delete_entity_authenticated(self):
        """Trying to delete an entity being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        entity = Entity.objects.first()
        response = self.client.delete('/api/v1/entities/{}'.format(entity.pk))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         'response from /api/1/entities has 403 Forbidden.')
