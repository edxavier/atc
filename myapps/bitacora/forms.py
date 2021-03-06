from django.forms import Select, Textarea
from myapps.accounts.models import Usuario
from myapps.catalogs.models import Turn, Dependency

__author__ = 'edx'
from django import forms
from .models import Note


class OpenNoteForm(forms.ModelForm):

    #dependency = forms.ModelChoiceField(queryset=Dependency.objects.filter(pk=1))

    class Meta:
        model = Note
        exclude = ('closed_at', 'created_by', 'open')
        widgets = {
            'dependency': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'note_model.dependency', 'required': True,
                                        'style':'width:100%', 'ng-change':'filter_user_pos(note_model.dependency)'}),
            'turn': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'note_model.turn', 'required': True, 'style':'width:100%'}),
            'position1': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'note_model.position1', 'required': True, 'style':'width:100%'}),
            'position2': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'note_model.position2', 'required': True, 'style':'width:100%'}),
            'position3': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'note_model.position3', 'required': True, 'style':'width:100%'}),
            'annotations_tags': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'note_model.annotations', 'style':'width:100%',}),
            'description': Textarea(attrs={'ng-model': 'note_model.description', 'rows': 4}),
        }

class SearchNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('closed_at', 'created_by', 'open')
        widgets = {
            'turn': Select(attrs={ 'ng-model': 'search.turn'}),
            'dependency': Select(attrs={ 'ng-model': 'search.dependency', 'class': 'ui search dropdown', }),
            'position1': Select(attrs={ 'ng-model': 'search.position1', 'class': 'ui search dropdown', }),
            'position2': Select(attrs={'ng-model': 'search.position2', 'class': 'ui search dropdown', }),
            'annotations_tags': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'search.annotations', 'style':'width:100%',}),

        }

class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('closed_at', 'created_by', 'open')
        widgets = {
            'annotations_tags': Select(attrs={'class': 'ui search dropdown', 'ng-model': 'note.annotations', 'style':'width:100%'}),
        }

