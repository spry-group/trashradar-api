import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from accounts import factories, models


# URLs
@pytest.fixture
def url_accounts():
    """
    Fixture responsible for build the api url for main endpoint
    Returns Func:
    """
    return reverse('accounts-list')


@pytest.fixture
def url_login():
    """
    Fixture responsible for build the api url for login endpoint
    Returns Func:
    """
    return reverse('login')


@pytest.fixture
def url_logout():
    """
    Fixture responsible for build the api url for logout endpoint
    Returns Func:
    """
    return reverse('logout')


@pytest.fixture
def url_detail():
    """
    Fixture responsible for build the api url for detail endpoint
    Returns Func:
    """

    def wrapper(pk):
        return reverse('accounts-detail', args=[pk])

    return wrapper


@pytest.fixture
def url_change_password():
    """
    Fixture responsible for build the api url for change password endpoint
    Returns Func:
    """

    def wrapper(pk):
        return reverse('accounts-change-password', args=[pk])

    return wrapper


@pytest.fixture
def client():
    """
    Fixture responsible for build the api client
    Returns APIClient object:
    """
    return APIClient()


# Factories
@pytest.fixture
def admin_account():
    """
    Fixture responsible for build an admin account
    Returns Account Object:
    """
    obj = factories.AccountFactory.create()
    obj.decrypt_password = obj.password
    obj.set_password(obj.password)
    obj.is_staff = True
    obj.is_admin = True
    obj.save()
    return obj


@pytest.fixture
def account():
    """
    Fixture responsible for build an account
    Returns Account Object:

    """
    obj = factories.AccountFactory.create()
    obj.decrypt_password = obj.password
    obj.set_password(obj.password)
    obj.save()
    return obj


# User Test Cases
@pytest.mark.django_db
def test_client_add_account_valid(client, url_accounts):
    """
    Testing add new account correctly
    Args:
        client: ApiClient
        url:  Endpoint Url,
        monkeypatch: Mock
    """
    data = {
        'full_name': factories.faker.name(),
        'email': factories.faker.email(),
        'username': factories.faker.email(),
        'phone': factories.faker.phone_number(),
        'password': factories.faker.password()
    }
    request = client.post(path=url_accounts, data=data, format='json')
    obj = models.Account.objects.get(email=data.get('email'))
    assert request.status_code == status.HTTP_201_CREATED, 'Fails to create account'
    assert models.Account.objects.count() == 1, 'Count is different in db'
    assert obj.check_password(data.get('password')) is True, 'The password do not match'
    assert obj.email == data.get('email'), 'The email do not match'
    assert obj.full_name == data.get('full_name'), 'The name do not match'
    assert obj.is_verified is False, 'The user is verified'
    assert '_auth_user_id' not in client.session._session, 'User is authenticaded'
