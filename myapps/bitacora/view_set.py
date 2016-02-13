from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import django_filters
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param

__author__ = 'edx'
from rest_framework import viewsets
from rest_framework import status
from .serializers import *
from rest_framework import pagination
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin, CreateModelMixin
import math
from rest_framework.permissions import DjangoModelPermissions, BasePermission

class PermsBinnacle(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.has_perm('bitacora.can_list')
        elif request.method == "POST":
            try:
                if request.user.has_perm('bitacora.add_note'):
                    depend = request.data["dependency"]
                    if depend == '1':
                        return request.user.has_perm('bitacora.can_relate_twr')
                    else:
                        return request.user.has_perm('bitacora.can_relate_app')
                else:
                    return request.user.has_perm('bitacora.add_note')
            except:
                return True
        elif request.method == "PUT":
            return True


class CustomNotesPaginator(pagination.PageNumberPagination):
    display_page_controls = True

    def get_paginated_response(self, data):
        #Calcular total de paginas
        res =(math.ceil(float(self.page.paginator.count)/float(self.page_size)))
        return Response({'count': int(res),
                         'records': self.page.paginator.count,
                         'number': self.page.number,
                         'next': self.get_next_link(),
                         'previous': self.get_previous_link(),
                         'results': data})

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return replace_query_param('', self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return replace_query_param('', self.page_query_param, page_number)


class NotesFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(name="created_at", lookup_type='gte')
    max_date = django_filters.DateFilter(name="created_at", lookup_type='lte')
    description = django_filters.CharFilter(name="description", lookup_type='icontains')

    class Meta:
        model = Note
        fields = ['min_date', 'max_date', 'dependency', 'turn', 'position2', 'position1', 'description','annotations_tags']


class NotesPaginatedViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-id')
    serializer_class = NoteSerializer
    pagination_class = CustomNotesPaginator
    filter_fields = ('dependency', )
    #permission_classes = (PermsBinnacle,)


class NotesViewSet(DjangoModelPermissions, ListModelMixin, UpdateModelMixin,
                   RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = Note.objects.all().order_by('-id')
    serializer_class = NoteSerializer
    filter_class = NotesFilter
    permission_classes = (PermsBinnacle,)

    def list(self, request, *args, **kwargs):
        notes = self.filter_queryset(Note.objects.all().order_by('-id'))
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        note_data = request.data


        note_data['created_by'] = user.id
        serial = NoteSerializer(data=note_data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        else:
            return Response(serial.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = NoteSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
