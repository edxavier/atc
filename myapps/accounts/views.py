from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView
from .models import Usuario
#from django.http import JsonResponse

from .forms import ModificarPerfilForm, CambiarClaveForm
from django.contrib.auth import login, logout, authenticate


# Create your views here.
class UserAccountData(UpdateView):
    model = Usuario
    template_name = "accounts/user_profile.html"
    fields = ["first_name", "last_name",]
    success_url = "/"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Usuario, pk=self.request.user.id)
        return obj

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if self.request.user.is_superuser:
            user_perms = Permission.objects.all()
        else:
            user_perms = self.request.user.user_permissions.all() | Permission.objects.filter(group__user=self.request.user)

        return render_to_response('accounts/user_profile.html', locals(),
            context_instance=RequestContext(request))


class ChangepasswordForm (View):
    def get(self, request):
        form = CambiarClaveForm(user=request.user)
        return render_to_response('accounts/change_passwd.html', locals(),
            context_instance=RequestContext(request))

    def post(self, request):
        form = CambiarClaveForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return render_to_response('accounts/change_passwd.html',
                locals(), context_instance=RequestContext(request))
