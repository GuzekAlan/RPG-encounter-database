from django.urls import path
from rpg_encounter.encounters.views import IndexView, CreateDatabaseView, TestFormView

app_name = 'encounters'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('create_database', CreateDatabaseView.as_view(), name="create_database"),
    path('test_form', TestFormView.as_view(), name="test_form")
]