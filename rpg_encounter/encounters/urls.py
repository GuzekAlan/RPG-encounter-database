from django.urls import path
from rpg_encounter.encounters import views


app_name = 'encounters'

urlpatterns = [
    path('', views.index, name="index"),
    path('create_database', views.create_database, name="create_database")
]
