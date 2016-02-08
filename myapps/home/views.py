from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render_to_response

# Create your views here.
from myapps.bitacora.models import Note
from myapps.bitacora.forms import OpenNoteForm, EditNoteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        form = OpenNoteForm()
        edit_form = EditNoteForm()
        #notas_list = Note.objects.all().order_by('-id')
        #paginator = Paginator(notas_list, 2) # Show 25 notes per page
        #page = request.GET.get('page')
        try:
            #notas = paginator.page(page)
            pass
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            #notas = paginator.page(1)
            pass
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            #notas = paginator.page(paginator.num_pages)
            pass
        return render_to_response(
            'main/home.html', locals(), context_instance=RequestContext(request)
        )