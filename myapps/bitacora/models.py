# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from atc.settings import AUTH_USER_MODEL
from myapps.catalogs.models import *
# Create your models here.


class Note(models.Model):
    open = models.BooleanField(default=True, verbose_name='¿Abierta?')
    turn = models.ForeignKey(Turn, verbose_name="Turno")
    dependency = models.ForeignKey(Dependency, verbose_name='Dependencia')
    position1 = models.ForeignKey(AUTH_USER_MODEL, related_name="position1", verbose_name='Posicion 1')
    position2 = models.ForeignKey(AUTH_USER_MODEL, related_name="position2", verbose_name='Posicion 2')
    description = models.TextField(blank=True, verbose_name='Descripcion')
    annotations_tags = models.ManyToManyField(AnnotationType, 'Tags', blank=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at =  models.DateTimeField(auto_now=True, verbose_name="Ultima actualizacion")


    class Meta:
        verbose_name_plural = 'Notas'
        verbose_name = 'Nota'
        permissions = (
            ("can_list", "Puede ver listado de notas"),
            ("can_search", " Puede buscar notas"),
            ("can_relate_twr", "Puede agregar notas a dependencia de TWR"),
            ("can_relate_app", "Puede agregar notas a dependencia de APP"),
            ("can_export", "Puede exportar una o varias notas a pdf"),
        )

    def __unicode__(self):
        return "Entrada " + str(self.pk)