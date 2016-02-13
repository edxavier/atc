from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render_to_response

# Create your views here.
from myapps.accounts.models import Usuario
from myapps.bitacora.models import Note
from myapps.bitacora.forms import OpenNoteForm, EditNoteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myapps.catalogs.models import Dependency


class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        param = request.GET.get('dependency', '')

        print(param)
        form = OpenNoteForm()
        form.fields['dependency'].empty_label = "Seleccione..."
        form.fields['turn'].empty_label = "Seleccione..."
        form.fields['position1'].empty_label = "Seleccione..."
        form.fields['position2'].empty_label = "Seleccione..."
        form.fields['annotations_tags'].empty_label = "Seleccione..."
        if not request.user.is_superuser:
            app = Usuario.objects.filter(groups__name__in=['aproximacion'], pk=request.user.id)
            twr = Usuario.objects.filter(groups__name__in=['torre'], pk=request.user.id)

            if len(app)>0 and len(twr) > 0:
                form.fields['dependency'].queryset = Dependency.objects.all()
            elif  len(app)>0:
                form.fields['dependency'].queryset = Dependency.objects.filter(pk=2)
            elif  len(twr)>0:
                form.fields['dependency'].queryset = Dependency.objects.filter(pk=1)

        edit_form = EditNoteForm()
        edit_form.fields['annotations_tags'].empty_label = "Seleccione..."
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