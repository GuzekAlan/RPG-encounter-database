from typing import Any, Dict
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse
from django.db import connection
from rpg_encounter.utils import executeScriptsFromFile
from os import path


class TestFormView():
    pass

class IndexView(TemplateView):
    template_name="base.html"
        
class CreateDatabaseView(TemplateView):
    template_name="create_database.html"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        with connection.cursor() as cursor:
            executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DDL.sql'), cursor=cursor)
        context = super().get_context_data(**kwargs)
        return context
