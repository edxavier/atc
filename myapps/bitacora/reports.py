from django.http import HttpResponseRedirect

__author__ = 'edx'

from django.shortcuts import get_object_or_404
from django.views.generic import View
from myapps.home.utils import html_to_pdf, link_callback
from .models import *
import json
from django.contrib.auth.mixins import PermissionRequiredMixin

class NotePdf(PermissionRequiredMixin, View):
    permission_required = ('bitacora.can_export',)
    raise_exception = True
    def get(self, request, note_pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=note_pk)
        return html_to_pdf("bitacora/note_pdf.html", locals())

class NotesPdf(PermissionRequiredMixin, View):
    permission_required = ('bitacora.can_export',)
    raise_exception = True

    def get(self, request, *args, **kwargs):
        json_ids = request.GET['vars']
        array_ids = json.loads(json_ids)
        notes = Note.objects.filter(pk__in=array_ids).order_by('-id')
        return html_to_pdf("bitacora/notes_pdf.html", locals())
