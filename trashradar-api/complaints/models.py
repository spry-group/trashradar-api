from django.db import models


class Entity(models.Model):
    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

    name = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    phone = models.CharField(blank=True, max_length=20, null=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
