from django import forms
from os import path
from rpg_encounter.sql_utils import saveData, getIdName, connectManyToMany, getMaxIndex


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


class RaceForm(forms.Form):
    """Form for encounters.rasy"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa rasy"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis"
    )
    terrains = forms.MultipleChoiceField(
        choices=getIdName('tereny'),
        widget=forms.CheckboxSelectMultiple,
        label="Zamieszkiwane tereny"
    )
    
    def save_record(self):
        if not saveData("rasy", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description']):
            return connectManyToMany('rasa_teren', [getMaxIndex('rasy')], self.cleaned_data['terrains'])
        return 0

class MonsterForm(forms.Form):
    """Form for encounters.potwory"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa potwora"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis"
    )
    lvl = forms.IntegerField(
        max_value=10,
        min_value=0,
        label="Poziom trudności"
    )
    race = forms.ChoiceField(
        choices=getIdName("rasy"),
        label="Rasa"
    )
    
    def save_record(self):
        return saveData("potwory", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description'],
                 poziom_trudnosci=self.cleaned_data['lvl'],
                 id_rasa=self.cleaned_data['race'])    


class TrapForm(forms.Form):
    """Form for encounters.pulapki"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa pułapki"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis"
    )
    lvl = forms.IntegerField(
        max_value=10,
        min_value=0,
        label="Poziom trudności"
    )

    def save_record(self):
        return saveData("pulapki", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description'],
                 poziom_trudnosci=self.cleaned_data['lvl'])    


class EncounterForm(forms.Form):
    """Form for encounters.potyczki"""
    title = forms.CharField(
        max_length=100,
        label="Nazwa potyczki"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis"
    )
    location = forms.ChoiceField(
        choices=getIdName('lokacje'),
        label="Lokacja"
    )
    monsters = forms.MultipleChoiceField(
        choices=getIdName('potwory'),
        widget=forms.CheckboxSelectMultiple,
        label="Potwory"
    )
    treasures = forms.MultipleChoiceField(
        choices=getIdName('skarby'),
        widget=forms.CheckboxSelectMultiple,
        label="Skarby"
    )
    traps = forms.MultipleChoiceField(
        choices=getIdName('pulapki'),
        widget=forms.CheckboxSelectMultiple,
        label="Pułapki"
    )
    def save_record(self):
        if not saveData("potyczki", 
                 tytul=self.cleaned_data['title'], 
                 opis=self.cleaned_data['description'],
                 id_lokacja=self.cleaned_data['location']
                 ):
            return all([connectManyToMany('potwor_potyczka', self.cleaned_data['monsters'], [getMaxIndex('potyczki')]),
                        connectManyToMany('skarb_potyczka', self.cleaned_data['treasures'], [getMaxIndex('potyczki')]),
                        connectManyToMany('pulapka_potyczka', self.cleaned_data['traps'], [getMaxIndex('potyczki')]),
                    ])
        print('chuj')
        return 0


    
    

    
    