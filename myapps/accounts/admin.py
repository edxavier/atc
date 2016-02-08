from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import UserCreationForm, UserChangeForm

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('username', 'is_staff', 'is_active')

    fieldsets = (
        ('Informacion de Acceso', {'fields': ('username', 'password')}),
        ('Informacion Personal', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permisos', {'fields': (('is_staff', 'is_superuser', 'is_active'), 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ("Informacion de la cuenta", {'fields': ('username','password1', 'password2')}),
        ("Informacion de contacto. Se enviara la informacion de acceso al correo si se especificare",
         {'fields': ('email',)}),
    )

    search_fields = ('email',)
    ordering = ('username', 'email',)
    filter_horizontal = ('groups', 'user_permissions',)



