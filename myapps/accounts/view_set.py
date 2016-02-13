__author__ = 'edx'
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()


    def list(self, request, *args, **kwargs):
        queryset = Usuario.objects.all()
        dependency = self.request.query_params.get('dependency', None)
        if dependency is not None and len(dependency)>0:
            if dependency == '1':
                queryset = Usuario.objects.filter(groups__name__in=['torre'])
            else:
                queryset = Usuario.objects.filter(groups__name__in=['aproximacion'])
        serializer = UsuarioSerializer(queryset, many=True)
        return Response(serializer.data)

