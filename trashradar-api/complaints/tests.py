import json
import mock
from io import BytesIO
from PIL import Image
from django.contrib.gis.geos import Point

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
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
    api_version = 'v1'
    fixtures = ['complaints', 'entities', 'accounts']

    @property
    def complaint_list_view_name(self):
        return self.api_version + ':complaint-list'

    @property
    def complaint_confirm_view_name(self):
        return self.api_version + ':complaint-confirm'

    @property
    def complaint_clean_view_name(self):
        return self.api_version + ':complaint-clean'

    def setUp(self):
        self.tmp_picture = SimpleUploadedFile(name='logo.jpg', content=image_string, content_type='image/jpeg')
        self.complaint = {
            'owner': 1,
            'entity': 1,
            'location': json.dumps({
                'type': 'Point',
                'coordinates': [
                    11.266675,
                    -74.189093
                ]
            }),
            'picture': self.tmp_picture,
            'tweet_status': [1]
        }
        self.cloudinary_image = {
            'public_id': 'x2ojoy5hc4x78y3ida1f', 'version': 1496421068,
            'signature': '8aa8f1031a19f15023548967ede58b5c7ba94fd2', 'width': 1, 'height': 1,
            'format': 'jpg', 'resource_type': 'image', 'created_at': '2017-06-02T16:31:08Z',
            'tags': [], 'bytes': 631, 'type': 'upload', 'etag': '2775f338c469b19c338c4e0ea410271c',
            'url': 'http://res.cloudinary.com/dsxvepxmc/image/upload/v1496421068/x2ojoy5hc4x78y3ida1f.jpg',
            'secure_url': 'https://res.cloudinary.com/dsxvepxmc/image/upload/v1496421068/x2ojoy5hc4x78y3ida1f.jpg',
            'original_filename': 'logo'
        }

    def tearDown(self):
        self.tmp_picture.close()

    def test_list_complaints_unauthenticated(self):
        """Fetch all the complaints"""
        response = self.client.get(reverse(self.complaint_list_view_name))
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'response from {} has 200 Ok.'.format(reverse(self.complaint_list_view_name)))

        returned_complaint = stored_data['results'][0]
        self.assertIn('id', returned_complaint, 'Id is not present on the result data')
        complaint = Complaint.objects.get(pk=returned_complaint['id'])

        self.assertEqual(complaint.counter, returned_complaint['counter'], 'Name does not match')

    def test_create_complaint_unauthenticated(self):
        """Trying to create a complaint being unauthenticated"""
        response = self.client.post(reverse(self.complaint_list_view_name), self.complaint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from {} is not 401 Unauthorized.'.format(reverse(self.complaint_list_view_name)))

    @mock.patch('cloudinary.uploader.upload')
    def test_create_complaint_authenticated(self, cloudinary_mock):
        """Creating a complaint being authenticated"""
        cloudinary_mock.return_value = self.cloudinary_image
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        response = self.client.post(reverse(self.complaint_list_view_name), self.complaint)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'response from {} is not 201.'.format(reverse(self.complaint_list_view_name)))

        complaint = Complaint.objects.get(pk=response.data['id'])
        self.assertIn('location', response.data, 'Location is not being returned.')
        location = response.data['location']
        self.assertIn('http://res.cloudinary.com/', str(response.data['picture']))
        self.assertEqual(type(complaint.location), Point)
        for coordinate in location['coordinates']:
            self.assertIn(coordinate, complaint.location.coords)

    @mock.patch('cloudinary.uploader.upload')
    def test_create_complaint_invalid_cloudinary(self, cloudinary_mock):
        """Trying to create a complaint being authenticated, but receiving an error from cloudinary"""
        cloudinary_mock.return_value = {}
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        response = self.client.post(reverse(self.complaint_list_view_name), self.complaint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         'response from {} is not 400.'.format(reverse(self.complaint_list_view_name)))

    def test_create_complaint_invalid_point(self):
        """Trying to create a complaint with an invalid point"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        complaint = self.complaint
        del complaint['location']
        response = self.client.post(reverse(self.complaint_list_view_name), complaint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         'response from {} is not 400.'.format(reverse(self.complaint_list_view_name)))

    def test_create_complaint_invalid_picture(self):
        """Trying to create a complaint with an invalid picture"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        complaint = self.complaint
        complaint['picture'] = 'test'
        response = self.client.post(reverse(self.complaint_list_view_name), complaint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         'response from {} is not 400.'.format(reverse(self.complaint_list_view_name)))

    def test_confirm_place_unauthenticated(self):
        """Trying to confirm a place being unauthenticated"""
        complaint = Complaint.objects.first()
        response = self.client.post(reverse(self.complaint_confirm_view_name, kwargs={'pk': complaint.pk}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from {} is not 401 Unauthorized.'.format(
                             reverse(self.complaint_confirm_view_name, kwargs={'pk': complaint.pk})))

    def test_confirm_place_authenticated(self):
        """Confirm a place being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        complaint = Complaint.objects.first()
        response = self.client.post(reverse(self.complaint_confirm_view_name, kwargs={'pk': complaint.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         'response from {} is not 204 No Content.'.format(
                             reverse(self.complaint_confirm_view_name, kwargs={'pk': complaint.pk})))

        updated_complaint = Complaint.objects.get(pk=complaint.pk)
        self.assertGreater(updated_complaint.counter, complaint.counter, 'The counter of the complaint is not updated')
        self.assertEqual(complaint.current_state, 1, 'The state of the complaint should be Active')

    def test_clean_place_unauthenticated(self):
        """Trying to clean a place being unauthenticated"""
        complaint = Complaint.objects.first()
        response = self.client.post(reverse(self.complaint_clean_view_name, kwargs={'pk': complaint.pk}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from {} is not 401 Unauthorized.'.format(
                             reverse(self.complaint_confirm_view_name, kwargs={'pk': complaint.pk})))

    def test_clean_place_authenticated(self):
        """Clean a place being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        complaint = Complaint.objects.first()
        response = self.client.post(reverse(self.complaint_clean_view_name, kwargs={'pk': complaint.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         'response from {} is not 204 No Content.'.format(
                             reverse(self.complaint_clean_view_name, kwargs={'pk': complaint.pk})))

        updated_complaint = Complaint.objects.get(pk=complaint.pk)
        self.assertEqual(complaint.counter, updated_complaint.counter, 'The counter of the complaint is different')
        self.assertNotEqual(complaint.current_state, 2, 'The state of the complaint should be Clean')


class EntitiesTestCase(APITestCase):
    """
    Entities tests
    """
    api_version = 'v1'
    fixtures = ['entities', 'accounts']

    @property
    def entity_list_view_name(self):
        return self.api_version + ':entity-list'

    @property
    def entity_detail_view_name(self):
        return self.api_version + ':entity-detail'

    def setUp(self):
        self.entity = {
            'name': 'New name',
            'twitter': 'newAccount',
            'phone': '987-654321',
            'template_message': 'New message'
        }

    def test_list_entities_unauthenticated(self):
        """Fetch all the entities"""
        response = self.client.get(reverse(self.entity_list_view_name))
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'response from {} has 200 Ok.'.format(reverse(self.entity_list_view_name)))

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
        response = self.client.get(reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk}))
        stored_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'response from {} has 200 Ok.'.format(
                             reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk})))

        self.assertEqual(entity.name, stored_data['name'], 'Name does not match')
        self.assertEqual(entity.twitter, stored_data['twitter'], 'Twitter does not match')
        self.assertEqual(entity.phone, stored_data['phone'], 'Phone does not match')
        self.assertNotIn('template_message', stored_data, 'Message is present on the result data')

    def test_create_entity_unauthenticated(self):
        """Trying to create an entity being unauthenticated"""
        response = self.client.post(
            reverse(self.entity_list_view_name),
            self.entity
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from {} has 401 Unauthorized.'.format(
                             reverse(self.entity_list_view_name)))

    def test_create_entity_authenticated(self):
        """Trying to create an entity being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        response = self.client.post(
            reverse(self.entity_list_view_name),
            self.entity
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         'response from {} has 403 Forbidden.'.format(
                             reverse(self.entity_list_view_name)))

    def test_update_entity_unauthenticated(self):
        """Trying to update an entity being unauthenticated"""
        entity = Entity.objects.first()
        response = self.client.put(
            reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk}),
            self.entity
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from {} has 401 Unauthorized.'.format(
                             reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk})))

    def test_update_entity_authenticated(self):
        """Trying to update an entity being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        entity = Entity.objects.first()
        response = self.client.put(
            reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk}),
            self.entity
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         'response from {} has 403 Forbidden.'.format(
                             reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk})))

    def test_delete_entity_unauthenticated(self):
        """Trying to delete an entity being unauthenticated"""
        entity = Entity.objects.first()
        response = self.client.delete(reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         'response from {} has 401 Unauthorized.'.format(
                             reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk})))

    def test_delete_entity_authenticated(self):
        """Trying to delete an entity being authenticated"""
        authenticated_user = Account.objects.get(username='user@trashradar.com')
        self.client.force_login(authenticated_user)

        entity = Entity.objects.first()
        response = self.client.delete(reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         'response from {} has 403 Forbidden.'.format(
                             reverse(self.entity_detail_view_name, kwargs={'pk': entity.pk})))
