from django import forms
from django.db import connection
from os import path
from rpg_encounter.utils import executeScriptsFromFile


class TestForm(forms.Form):
    """Test form for tereny table """
    name = forms.CharField(
        max_length=100,
        label="Nazwa terenu "
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis "
    )
    
    def save_record(self):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO encounters.tereny(nazwa, opis) VALUES(%s, %s)", [self.cleaned_data['name'], self.cleaned_data['description']])