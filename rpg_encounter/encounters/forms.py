from django import forms
from os import path
from rpg_encounter.sql_utils import saveData, getIdName, connectManyToMany, getMaxIndex, checkUser


class TerrainForm(forms.Form):
    """Form for encounters.tereny"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa terenu",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis",
        required=True
    )
    
    def save_record(self):
        return saveData("tereny", 
                 nazwa=self.cleaned_data['name'], 
                 opis=self.cleaned_data['description'])
            
            
            
            
class LocationForm(forms.Form):
    """Form for encounters.lokacje"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa lokacji",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis",
        required=True
    )
    terrain = forms.ChoiceField(
        choices=getIdName("tereny"),
        label="Teren",
        required=True
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
        label="Nazwa skarbu",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis",
        required=True
    )
    rarity = forms.CharField(
        max_length=100,
        label="Rzadkość",
        required=True
    )
    price = forms.IntegerField(
        max_value=1000000,
        min_value=0,
        label="Wartość skarbu",
        required=True
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
        label="Nazwa rasy",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis",
        required=True
    )
    terrains = forms.MultipleChoiceField(
        choices=getIdName('tereny'),
        widget=forms.CheckboxSelectMultiple,
        label="Zamieszkiwane tereny",
        required=True
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
        label="Nazwa potwora",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis",
        required=True
    )
    lvl = forms.IntegerField(
        max_value=10,
        min_value=0,
        label="Poziom trudności",
        required=True
    )
    race = forms.ChoiceField(
        choices=getIdName("rasy"),
        label="Rasa",
        required=True
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
        label="Nazwa pułapki",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis",
        required=True
    )
    lvl = forms.IntegerField(
        max_value=10,
        min_value=0,
        label="Poziom trudności",
        required=True
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
        label="Tytuł potyczki",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        label="Krótki opis",
        required=True
    )
    location = forms.ChoiceField(
        choices=getIdName('lokacje'),
        label="Lokacja",
        required=True
    )
    monsters = forms.MultipleChoiceField(
        choices=getIdName('potwory'),
        widget=forms.CheckboxSelectMultiple,
        label="Potwory",
        required=True
    )
    treasures = forms.MultipleChoiceField(
        choices=getIdName('skarby'),
        widget=forms.CheckboxSelectMultiple,
        label="Skarby",
        required=True
    )
    traps = forms.MultipleChoiceField(
        choices=getIdName('pulapki'),
        widget=forms.CheckboxSelectMultiple,
        label="Pułapki",
        required=True
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


class UserRegisterForm(forms.Form):
    """Form form registering"""
    name=forms.CharField(
        max_length=100,
        label="Nazwa użytkownika",
        required=True
    )
    login=forms.CharField(
        max_length=50,
        label="Login",
        required=True
    )
    password=forms.CharField(
        max_length=50,
        label="Hasło",
        widget=forms.PasswordInput,
        required=True
    )
    def save_record(self):
        return saveData("osoby", 
            nazwa=self.cleaned_data['name'],
            login=self.cleaned_data['login'],
            haslo=self.cleaned_data['password'])
        

class UserLoginForm(forms.Form):
    """Form for encounters.osoby"""
    login=forms.CharField(
        max_length=50,
        label="Login",
        required=True
    )
    password=forms.CharField(
        max_length=50,
        label="Hasło",
        widget=forms.PasswordInput,
        required=True
    )
    def save_record(self):
        return checkUser(self.cleaned_data['login'], self.cleaned_data['password'])
    

    
    