from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AnnotationType(models.Model):
    name = models.CharField(max_length=400)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Turn(models.Model):
    name = models.CharField(max_length=400)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Dependency(models.Model):
    name = models.CharField(max_length=400)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

