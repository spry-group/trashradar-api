from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db.models import PointField

from accounts.models import Account


class Entity(models.Model):
    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

    name = models.CharField(max_length=200)
    twitter = models.CharField(max_length=20)
    phone = models.CharField(blank=True, max_length=20, null=True)
    template_message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        :return: Entity name
        """
        return self.name


class Complaint(models.Model):
    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    COMPLAINT_STATES = (
        (1, 'Dirty'),
        (2, 'Clean'),
    )

    owner = models.ForeignKey(Account)
    entity = models.ForeignKey(Entity)
    location = PointField()
    # URL to image stored in cloudinary
    picture = models.URLField()
    counter = models.IntegerField(default=0)
    current_state = models.IntegerField(choices=COMPLAINT_STATES, default=1)
    # List of tweet ids sent in the trashradar twitter account using the social_media util
    tweet_status = ArrayField(models.BigIntegerField(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
