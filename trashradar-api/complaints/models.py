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


class Complaint(models.Model):
    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    owner = models.ForeignKey(Account)
    entity = models.ForeignKey(Entity)
    location = PointField()
    picture = models.ImageField()
    counter = models.IntegerField(default=0)
    current_state = models.IntegerField(default=0)
    tweet_status = ArrayField(models.IntegerField())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
