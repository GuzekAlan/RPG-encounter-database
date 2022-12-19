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
    columns =[""]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select'] = getData(self.table_name, self.columns)
        context['column_names'] = self.columns
        return context
    
class TerrainTableView(SimpleTableView):
    table_name="tereny"
    columns=['nazwa', 'opis']

# Form views

class SimpleFormView(FormView):
    template_name="encounters_form.html"
    success_url='/'
    
    def form_valid(self, form):
        form.save_record()
        return super().form_valid(form)

class TerrainFormView(SimpleFormView):
    form_class=forms.TerrainForm
    
class LocationFormView(SimpleFormView):
    form_class=forms.LocationForm
    
class TreasureFormView(SimpleFormView):
    form_class=forms.TreasureForm