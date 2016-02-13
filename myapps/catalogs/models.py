from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AnnotationType(models.Model):
    name = models.CharField(max_length=400)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Tipos de Nota'
        verbose_name = 'Tipo de Nota'

    def __unicode__(self):
        return self.name


class Turn(models.Model):
    name = models.CharField(max_length=400)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Turnos'
        verbose_name = 'Turno'

    def __unicode__(self):
        return self.name

class Dependency(models.Model):
    name = models.CharField(max_length=400)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Dependencias'
        verbose_name = 'Dependencia'

    def __unicode__(self):
        return self.name

