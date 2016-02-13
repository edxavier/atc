from pyexpat import model
from datetime import datetime

__author__ = 'edx'
from rest_framework import serializers
from myapps.accounts.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'first_name', 'last_name',)
