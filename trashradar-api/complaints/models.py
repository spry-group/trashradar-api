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


class Event(models.Model):
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    location = PointField()
    user = models.ForeignKey(Account)
    pictures = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirm = models.BooleanField()


class Complaint(models.Model):
    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    owner = models.ForeignKey(Account)
    tweet_status = ArrayField(models.IntegerField())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
