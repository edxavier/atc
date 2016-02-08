from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views.generic import TemplateView
from myapps.bitacora.forms import SearchNoteForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class Search(PermissionRequiredMixin, TemplateView):
    permission_required = ('bitacora.can_search',)
    raise_exception = True

    def get(self, request, *args, **kwargs):
        form = SearchNoteForm()
        return render_to_response(
            'bitacora/note_search.html', locals(), context_instance=RequestContext(request)
        )
