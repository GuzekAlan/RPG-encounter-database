from django import forms
from os import path
from rpg_encounter.utils import executeScriptsFromFile, saveData, getData


class TerrainForm(forms.Form):
    """Form for encounters.tereny"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa terenu"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis"
    )
    
    def save_record(self):
        saveData("tereny", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description'])
            
            
            
class LocationForm(forms.Form):
    """Form for encounters.lokacje"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa lokacji"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis"
    )
    terrain = forms.ChoiceField(choices=getData("tereny"))
    
    def save_record(self):
        saveData("lokacje", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description'], 
                 id_teren=self.cleaned_data['terrain'])
    


