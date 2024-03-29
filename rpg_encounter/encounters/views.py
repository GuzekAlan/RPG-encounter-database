from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, View
from rpg_encounter.encounters import forms
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rpg_encounter.sql_utils import (
    execute_scripts_from_file,
    get_data,
    get_encounter_by_creator, get_encounter_by_creator_filter,
)
from os import path


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.get_signed_cookie(key="auth", default=None)
        return context


class CreateDatabaseView(TemplateView):
    template_name = "create_database.html"

    def get_context_data(self, **kwargs):
        execute_scripts_from_file(path.join(path.dirname(__file__), "sql/DDL.sql"))
        print("DDL EXECUTED")
        execute_scripts_from_file(path.join(path.dirname(__file__), "sql/DML.sql"))
        print("DML EXECUTED")
        context = super().get_context_data(**kwargs)
        return context


# Table views


class SimpleTableView(TemplateView):
    template_name = "encounters_table.html"

    table_name = ""
    dbColumns = ["*"]
    tableColumns = [""]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["select"] = get_data(self.table_name, self.dbColumns)
        context["column_names"] = self.tableColumns
        return context


class TerrainTableView(SimpleTableView):
    table_name = "tereny_widok"
    tableColumns = ["Nazwa Terenu", "Krótki opis"]



class LocationTableView(SimpleTableView):
    table_name = "lokacje_widok"
    tableColumns = ["Nazwa Lokacji", "Krótki opis", "Teren"]


class TreasureTableView(SimpleTableView):
    table_name = "skarby_widok"
    tableColumns = ["Nazwa Skarbu", "Krótki opis", "Rzadkość", "Wartość(g)"]


class RaceTableView(SimpleTableView):
    table_name = "rasy_widok"
    tableColumns = ["Nazwa Rasy", "Krótki opis", "Zamieszkiwane tereny"]


class MonsterTableView(SimpleTableView):
    table_name = "potwory_widok"
    tableColumns = [
        "Nazwa Potwora",
        "Krótki opis",
        "Poziom trudności",
        "Rasa",
        "Zamieszkiwane tereny",
    ]


class TrapTableView(SimpleTableView):
    table_name = "pulapki_widok"
    tableColumns = ["Nazwa Pułapki", "Krótki opis", "Poziom trudności"]


class EncounterTableView(TemplateView):
    template_name = "encounters_table.html"
    tableColumns = [
        "Nazwa Potyczki",
        "Krótki opis",
        "Lokacja",
        "Potwory",
        "Pułapki",
        "Skarby",
        "Poziom Trudności",
        "Nazwa twórcy",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["select"] = get_encounter_by_creator(
            self.request.get_signed_cookie("auth", default=None)
        )
        context["column_names"] = self.tableColumns
        return context


# Form views


class SimpleFormView(FormView):
    template_name = "encounters_form.html"
    success_url = "/"
    message = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = self.message
        return context

    def form_valid(self, form):
        response = form.save_record()
        if response == 0:
            return super(SimpleFormView, self).form_valid(form)
        else:
            if response == -1:
                self.message = "Podany rekord już istnieje"
            if response == -2:
                self.message = "Login lub hasło są niepoprawne"
            return super().form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class TerrainFormView(SimpleFormView):
    form_class = forms.TerrainForm


class LocationFormView(SimpleFormView):
    form_class = forms.LocationForm


class TreasureFormView(SimpleFormView):
    form_class = forms.TreasureForm


class RaceFormView(SimpleFormView):
    form_class = forms.RaceForm


class MonsterFormView(SimpleFormView):
    form_class = forms.MonsterForm


class TrapFormView(SimpleFormView):
    form_class = forms.TrapForm


class EncounterFormView(SimpleFormView):
    form_class = forms.EncounterForm

    def get_form_kwargs(self):
        kw = super(EncounterFormView, self).get_form_kwargs()
        kw["request"] = self.request
        return kw

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.get_signed_cookie(key="auth", default=None)
        return context


class UserRegisterFormView(SimpleFormView):
    form_class = forms.UserRegisterForm


class UserLoginFormView(SimpleFormView):
    form_class = forms.UserLoginForm

    def form_valid(self, form):
        user = form.log_in()
        if user:
            response = HttpResponseRedirect(self.success_url)
            response.set_signed_cookie("auth", value=user, max_age=60 * 60 * 3)
            return response
        else:
            self.message = "Login lub hasło są niepoprawne"
            return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        response = HttpResponseRedirect("/")
        response.delete_cookie("auth")
        return response


# Delete vies

class DeleteFormView(FormView):

    template_name = "delete_form.html"
    success_url = "/"
    message = ""
    table_name = ""
    id_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = self.message
        return context

    def form_valid(self, form):
        form.delete_record()
        return super().form_valid(form)


class DeleteTerrainView(DeleteFormView):
    table_name = "tereny"
    form_class = forms.create_delete_form(table_name)


class DeleteLocationView(DeleteFormView):
    table_name = "lokacje"
    form_class = forms.create_delete_form(table_name)


class DeleteTreasureView(DeleteFormView):
    table_name = "skarby"
    form_class = forms.create_delete_form(table_name)


class DeleteTrapView(DeleteFormView):
    table_name = "pulapki"
    form_class = forms.create_delete_form(table_name)


class DeleteRaceView(DeleteFormView):
    table_name = "rasy"
    form_class = forms.create_delete_form(table_name)


class DeleteMonsterView(DeleteFormView):
    table_name = "potwory"
    form_class = forms.create_delete_form(table_name)



class DeleteEncounterView(DeleteFormView):
    form_class = forms.DeleteEncounterForm

    def get_form_kwargs(self):
        kw = super(DeleteEncounterView, self).get_form_kwargs()
        kw["request"] = self.request
        return kw


# Other views

class EncounterFilteredView(TemplateView):
    template_name = "encounters_filtered_table.html"

    tableColumns = [
        "Nazwa Potyczki",
        "Krótki opis",
        "Lokacja",
        "Potwory",
        "Pułapki",
        "Skarby",
        "Poziom Trudności",
        "Nazwa twórcy",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["column_names"] = self.tableColumns
        # context["min_lvl"] = 0
        # context["max_lvl"] = 100
        context["min_lvl"] = self.request.GET.get('min_lvl', default=0)
        context["max_lvl"] = self.request.GET.get('max_lvl', default=100)
        context["select"] = get_encounter_by_creator_filter(
            self.request.get_signed_cookie("auth", default=None),
            context["min_lvl"],
            context["max_lvl"]
        )
        return context