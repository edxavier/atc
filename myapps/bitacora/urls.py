__author__ = 'edx'

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import Search
from .reports import NotePdf, NotesPdf

binnacle_patterns = [
    url(r'^advaced_search/$', login_required(Search.as_view()), name='notes_search'),
    url(r'^report/(\d+)/$', login_required(NotePdf.as_view()),name='note_report'),
    url(r'^report/notes/$', login_required(NotesPdf.as_view()),name='notes_report'),
]
