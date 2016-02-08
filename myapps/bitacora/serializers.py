from pyexpat import model
from datetime import datetime

__author__ = 'edx'
from rest_framework import serializers
from .models import Note
from myapps.accounts.models import Usuario


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'first_name', 'last_name',)

class NoteSerializer(serializers.ModelSerializer):
    controler1 = serializers.SerializerMethodField(source='get_controler1')
    controler2 = serializers.SerializerMethodField(source='get_controler2')
    controler0 = serializers.SerializerMethodField(source='get_controler0')

    def get_controler0(self, obj):
        if(obj.created_by.first_name):
            return obj.created_by.first_name + " " + obj.created_by.last_name
        else:
            return obj.created_by.username

    def get_controler1(self, obj):
        if(obj.position1.first_name):
            return obj.position1.first_name + " " + obj.position1.last_name
        else:
            return obj.position1.username

    def get_controler2(self, obj):
        if(obj.position2.first_name):
            return obj.position2.first_name + " " + obj.position2.last_name
        else:
            return obj.position2.username

    def validate(self, attrs):
        try:
            turn = attrs['turn']
            dependency = attrs['dependency']
            count = Note.objects.filter(created_at__contains=datetime.date(datetime.now()),
                                        turn=turn, dependency=dependency).count()
            if count > 0:
                raise serializers.ValidationError("Ya existe una nota asociada al turno "
                                                  "y dependencia especificada para el dia de hoy")
        except Exception, e:
            return attrs
        return attrs

    class Meta:
        model = Note
        #depth = 1