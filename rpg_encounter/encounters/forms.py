from django import forms
from os import path
from rpg_encounter.sql_utils import save_data, get_id_name, connect_many_to_many, get_max_index, check_user


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
        return save_data("tereny",
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
        choices=get_id_name("tereny"),
        label="Teren",
        required=True
    )

    def save_record(self):
        return save_data("lokacje",
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
        return save_data("skarby",
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
        choices=get_id_name('tereny'),
        widget=forms.CheckboxSelectMultiple,
        label="Zamieszkiwane tereny",
        required=True
    )

    def save_record(self):
        if not save_data("rasy",
                         nazwa=self.cleaned_data['name'],
                         opis=self.cleaned_data['description']):
            return connect_many_to_many('rasa_teren', [get_max_index('rasy')], self.cleaned_data['terrains'])
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
        choices=get_id_name("rasy"),
        label="Rasa",
        required=True
    )

    def save_record(self):
        return save_data("potwory",
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
        return save_data("pulapki",
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
        choices=get_id_name('lokacje'),
        label="Lokacja",
        required=True
    )
    monsters = forms.MultipleChoiceField(
        choices=get_id_name('potwory'),
        widget=forms.CheckboxSelectMultiple,
        label="Potwory",
        required=True
    )
    treasures = forms.MultipleChoiceField(
        choices=get_id_name('skarby'),
        widget=forms.CheckboxSelectMultiple,
        label="Skarby",
        required=True
    )
    traps = forms.MultipleChoiceField(
        choices=get_id_name('pulapki'),
        widget=forms.CheckboxSelectMultiple,
        label="Pułapki",
        required=True
    )

    def save_record(self):
        if not save_data("potyczki",
                         tytul=self.cleaned_data['title'],
                         opis=self.cleaned_data['description'],
                         id_lokacja=self.cleaned_data['location']
                         ):
            return all(
                [connect_many_to_many('potwor_potyczka', self.cleaned_data['monsters'], [get_max_index('potyczki')]),
                 connect_many_to_many('skarb_potyczka', self.cleaned_data['treasures'], [get_max_index('potyczki')]),
                 connect_many_to_many('pulapka_potyczka', self.cleaned_data['traps'], [get_max_index('potyczki')]),
                 ])
        print('chuj')
        return 0


class UserRegisterForm(forms.Form):
    """Form for registering"""
    name = forms.CharField(
        max_length=100,
        label="Nazwa użytkownika",
        required=True
    )
    login = forms.CharField(
        max_length=50,
        label="Login",
        required=True
    )
    password = forms.CharField(
        max_length=50,
        label="Hasło",
        widget=forms.PasswordInput,
        required=True
    )

    def save_record(self):
        return save_data("osoby",
                         nazwa=self.cleaned_data['name'],
                         login=self.cleaned_data['login'],
                         haslo=self.cleaned_data['password'])


class UserLoginForm(forms.Form):
    """Form for encounters.osoby"""
    login = forms.CharField(
        max_length=50,
        label="Login",
        required=True
    )
    password = forms.CharField(
        max_length=50,
        label="Hasło",
        widget=forms.PasswordInput,
        required=True
    )

    def log_in(self):
        return check_user(self.cleaned_data['login'], self.cleaned_data['password'])
