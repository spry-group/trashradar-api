import json
from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Factory as FakerFactory
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account
from complaints.models import Complaint, Entity

faker = FakerFactory.create()

image_buffer = BytesIO()
test_image = Image.new('RGB', (1, 1))
test_image.save(image_buffer, 'jpeg')
image_buffer.seek(0)
image_string = image_buffer.read()


class ComplaintsTestCase(APITestCase):

    fixtures = ['complaints', 'entities', 'accounts']

    def setUp(self):
        self.tmp_picture = SimpleUploadedFile(name='logo.jpg', content=image_string, content_type='image/jpeg')
        self.complaint = {
            'owner': 1,
            'entity': 1,
            'location': 'SRID=4326;POINT (12 11)',
            'picture': self.tmp_picture,
            'tweet_status': [1]
        }

    def tearDown(self):
        self.tmp_picture.close()

    def test_list_complaints_unauthenticated(self):
        """Fetch all the complaints"""
        response = self.client.get('/api/v1/complaints')
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response from /api/1/complaints has 200 Ok.')

        returned_complaint = stored_data['results'][0]
        self.assertIn('id', returned_complaint, 'Id is not present on the result data')
        complaint = Complaint.objects.get(pk=returned_complaint['id'])

        self.assertEqual(complaint.counter, returned_complaint['counter'], 'Name does not match')

    def test_create_complaint_unauthenticated(self):
        """Trying to create a complaint being unauthenticated"""
        url = '/api/v1/complaints'
        response = self.client.post(url, self.complaint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from /api/1/complaints is not 401 Unauthorized.')

    def test_create_complaint_authenticated(self):
        """Trying to create a complaint being authenticated"""
        url = '/api/v1/complaints'
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        response = self.client.post(url, self.complaint)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'response from /api/1/complaints is not 201.')

    def test_confirm_place_unauthenticated(self):
        """Trying to confirm a place being unauthenticated"""
        complaint = Complaint.objects.first()
        response = self.client.post('/api/v1/complaints/{}/confirm'.format(complaint.pk))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from /api/1/complaints is not 401 Unauthorized.')

    def test_confirm_place_authenticated(self):
        """Confirm a place being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        complaint = Complaint.objects.first()
        response = self.client.post('/api/v1/complaints/{}/confirm'.format(complaint.pk))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         'response from /api/1/complaints is not 204 No Content.')

        updated_complaint = Complaint.objects.get(pk=complaint.pk)
        self.assertGreater(updated_complaint.counter, complaint.counter, 'The counter of the complaint is not updated')
        self.assertEqual(complaint.current_state, 1, 'The state of the complaint should be Active')

    def test_clean_place_unauthenticated(self):
        """Trying to clean a place being unauthenticated"""
        complaint = Complaint.objects.first()
        response = self.client.post('/api/v1/complaints/{}/clean'.format(complaint.pk))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from /api/1/complaints is not 401 Unauthorized.')

    def test_clean_place_authenticated(self):
        """Clean a place being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        complaint = Complaint.objects.first()
        response = self.client.post('/api/v1/complaints/{}/clean'.format(complaint.pk))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         'response from /api/1/complaints is not 204 No Content.')

        updated_complaint = Complaint.objects.get(pk=complaint.pk)
        self.assertEqual(complaint.counter, updated_complaint.counter, 'The counter of the complaint is different')
        self.assertNotEqual(complaint.current_state, 2, 'The state of the complaint should be Clean')


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
            self.entity
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from /api/1/entities has 401 Unauthorized.')

    def test_create_entity_authenticated(self):
        """Trying to create an entity being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        response = self.client.post(
            '/api/v1/entities',
            self.entity
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         'response from /api/1/entities has 403 Forbidden.')

    def test_update_entity_unauthenticated(self):
        """Trying to update an entity being unauthenticated"""
        entity = Entity.objects.first()
        response = self.client.put(
            '/api/v1/entities/{}'.format(entity.pk),
            self.entity
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
            self.entity
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
