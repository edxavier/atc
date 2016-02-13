from django.contrib import admin
from .models import Note
# Register your models here.

@admin.register(Note)
class NotaAdmin (admin.ModelAdmin):
    list_display=('id','dependency','turn', 'created_by','created_at',  )
    list_filter=('open','dependency', 'turn')
    readonly_fields = ('update_at',)
    search_fields=('created_by__username','dependency__name',
                   'created_by__first_name','description')
    list_per_page = 10