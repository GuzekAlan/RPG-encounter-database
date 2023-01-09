from django.views.generic import TemplateView, FormView
from rpg_encounter.encounters import forms
from django.db import connection
from rpg_encounter.sql_utils import executeScriptsFromFile, getData
from os import path


class IndexView(TemplateView):
    template_name="index.html"
        
class CreateDatabaseView(TemplateView):
    template_name="create_database.html"
    
    def get_context_data(self, **kwargs):
        executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DDL.sql'))
        executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DML.sql'))
        context = super().get_context_data(**kwargs)
        return context
    
# Table views

class SimpleTableView(TemplateView):
    template_name="encounters_table.html"
    
    table_name = ""
    dbColumns =["*"]
    tableColumns = [""]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select'] = getData(self.table_name, self.dbColumns)
        context['column_names'] = self.tableColumns
        return context
    
class TerrainTableView(SimpleTableView):
    table_name="tereny_widok"
    tableColumns=["Nazwa Terenu", "Krótki opis"]

class LocationTableView(SimpleTableView):
    table_name="lokacje_widok" 
    tableColumns=['Nazwa Lokacji', 'Krótki opis', 'Teren']

class TreasureTableView(SimpleTableView):
    table_name="skarby_widok"
    tableColumns=["Nazwa Skarbu", "Krótki opis", "Rzadkość", "Wartość(g)"]

# Form views

class SimpleFormView(FormView):
    template_name="encounters_form.html"
    success_url='/'
    message = ""

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["message"] = self.message
            return context

    def form_valid(self, form):
        if not form.save_record():
            return super().form_valid(form)
        else:
            self.message = "Podany rekord już istnieje"
            return super().form_invalid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)
        

class TerrainFormView(SimpleFormView):
    form_class=forms.TerrainForm
    
class LocationFormView(SimpleFormView):
    form_class=forms.LocationForm
    
class TreasureFormView(SimpleFormView):
    form_class=forms.TreasureForm
