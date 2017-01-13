import factory
from faker import Factory as FakerFactory

from accounts.models import Account

faker = FakerFactory.create()


class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Account

    email = factory.LazyAttribute(lambda x: faker.email() + str(faker.unix_time()))
    username = factory.LazyAttribute(lambda x: faker.email() + str(faker.unix_time()))
    password = factory.LazyAttribute(lambda x: faker.md5())
    full_name = factory.LazyAttribute(lambda x: faker.name())
    phone = factory.LazyAttribute(lambda x: faker.numerify() * 12)
    is_active = True
    is_verified = True
