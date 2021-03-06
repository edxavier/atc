__author__ = 'edx'
from rest_framework import routers
from myapps.bitacora.view_set import *
from myapps.accounts.view_set import *

router = routers.DefaultRouter()
router.register(r'accounts/users', UserViewSet)
router.register(r'binnacle/pages', NotesPaginatedViewSet, base_name="binacle_pages")
router.register(r'binnacle/notes', NotesViewSet)
