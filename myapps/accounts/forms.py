# coding=utf-8
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Usuario


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)


    """telefono = forms.RegexField(regex='^[5-9]\d{3}-\d{4}',
                                error_message='Introduzca un numero de telefono valido con el formato requerido ',
                                help_text='Formato: ####-####, No se aceptan numeros convencionales.')"""
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma tu contraseña', widget=forms.PasswordInput)
    #password3 = forms.CharField(label='Confirma tu contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['email', 'password1', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las claves no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        usuario = super(UserCreationForm, self).save(commit=False)
        usuario.TEMP_PASSWD = self.cleaned_data["password1"]
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField( help_text=("Las claves no se almacenan en texto plano, asi que no hay manera"
                    "de ver la clave del usuario, pero se puede modificard "
                    "usando <a href=\"password/\">este formulario</a>."))

    class Meta:
        model = Usuario
        fields = []


    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ModificarPerfilForm(forms.ModelForm):
    """username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30,
                                    widget=forms.TextInput(attrs={
                                        'type' : 'password'
                                    }))"""
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "email")

class CambiarClaveForm(PasswordChangeForm):
    error_css_class = 'field error'
    required_css_class = 'field error'
    old_password = forms.CharField(label='Contraseña antigua ', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirma tu contraseña', widget=forms.PasswordInput)

