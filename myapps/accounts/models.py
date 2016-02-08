# coding=utf-8
from django.db import models
import os
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, User
)
from django.dispatch import receiver


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):

        #email = self.normalize_email(email)
        #if not email:
           # raise ValueError('El email es un campo requerido')
        user = self.model(username=username, is_active=True,
                          is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, verbose_name='Usuario')
    first_name = models.CharField(max_length=50, verbose_name='Nombres', blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Apellidos', blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Esta Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Es Administrador',
                                   help_text='Indica si el usuario puede acceder al panel de administracion')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    TEMP_PASSWD = ""

    '''class Meta:
        permissions = (
            ("ver_usuarios", "Puede ver la lista de usuarios"),
            ("change_task_status", "Can change the status of tasks"),
        )'''
    def __unicode__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_admin(self):
        return self.is_staff

    def is_super_user(self):
        return self.is_superuser

    def get_full_name(self):
        if self.first_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.username



