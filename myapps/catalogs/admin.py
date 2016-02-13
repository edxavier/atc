from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(AnnotationType)
class AnnotationAdmin (admin.ModelAdmin):
    list_display=('name', 'active')
    list_filter=('active',)
    search_fields=('name','active')
    list_per_page = 10

admin.site.register(Turn)
admin.site.register(Dependency)