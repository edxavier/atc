from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from atc.settings import AUTH_USER_MODEL
from myapps.catalogs.models import *
# Create your models here.


class Note(models.Model):
    open = models.BooleanField(default=True)
    turn = models.ForeignKey(Turn)
    dependency = models.ForeignKey(Dependency)
    position1 = models.ForeignKey(AUTH_USER_MODEL, related_name="position1")
    position2 = models.ForeignKey(AUTH_USER_MODEL, related_name="position2")
    description = models.TextField(blank=True)
    annotations_tags = models.ManyToManyField(AnnotationType)
    created_by = models.ForeignKey(AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Notas'
        permissions = (
            ("can_list", "Puede ver listado de notas"),
            ("can_search", " Puede buscar notas"),
            ("can_relate_twr", "Puede agregar notas a dependencia de TWR"),
            ("can_relate_app", "Puede agregar notas a dependencia de APP"),
            ("can_export", "Puede exportar una o varias notas a pdf"),
        )

    def __unicode__(self):
        return "Entrada " + str(self.pk)