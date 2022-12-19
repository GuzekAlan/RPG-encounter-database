from django.views.generic import TemplateView, FormView
from rpg_encounter.encounters.forms import TestForm
from django.db import connection
from rpg_encounter.utils import executeScriptsFromFile
from os import path


class TestFormView(FormView):
    template_name="encounters_form.html"
    form_class=TestForm
    success_url='/'
    
    def form_valid(self, form):
        form.save_record()
        return super().form_valid(form)

class IndexView(TemplateView):
    template_name="index.html"
        
class CreateDatabaseView(TemplateView):
    template_name="create_database.html"
    
    def get_context_data(self, **kwargs):
        with connection.cursor() as cursor:
            executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DDL.sql'), cursor=cursor)
            executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DML.sql'), cursor=cursor)
        context = super().get_context_data(**kwargs)
        return context
