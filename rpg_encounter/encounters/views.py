from django.views.generic import TemplateView, FormView
from rpg_encounter.encounters.forms import TerrainForm, LocationForm
from django.db import connection
from rpg_encounter.utils import executeScriptsFromFile
from os import path

class SimpleFormView(FormView):
    success_url='/'
    
    def form_valid(self, form):
        form.save_record()
        return super().form_valid(form)

class TerrainFormView(SimpleFormView):
    template_name="encounters_form.html"
    form_class=TerrainForm
    
class LocationFormView(SimpleFormView):
    template_name="encounters_form.html"
    form_class=LocationForm

class IndexView(TemplateView):
    template_name="index.html"
        
class CreateDatabaseView(TemplateView):
    template_name="create_database.html"
    
    def get_context_data(self, **kwargs):
        executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DDL.sql'))
        executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DML.sql'))
        context = super().get_context_data(**kwargs)
        return context
