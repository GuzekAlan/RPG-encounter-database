from django import forms
from os import path
from rpg_encounter.sql_utils import executeScriptsFromFile, saveData, getIdName


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
        return saveData("tereny", 
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
    terrain = forms.ChoiceField(
        choices=getIdName("tereny"),
        label="Teren"
    )
    
    def save_record(self):
        return saveData("lokacje", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description'], 
                 id_teren=self.cleaned_data['terrain'])
    
    
class TreasureForm(forms.Form):
    """Form for encounters.skarby"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa skarbu"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis"
    )
    rarity = forms.CharField(
        max_length=100,
        label="Rzadkość"
    )
    price = forms.IntegerField(
        max_value=1000000,
        min_value=0,
        label="Wartość skarbu"
    )
    
    def save_record(self):
        return saveData("skarby", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description'],
                 rzadkosc=self.cleaned_data['rarity'],
                 wartosc=self.cleaned_data['price'])


