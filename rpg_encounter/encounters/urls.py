from django.urls import path
from rpg_encounter.encounters import views

app_name = 'encounters'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('create_database', views.CreateDatabaseView.as_view(), name="create_database"),
    path('terrain_form', views.TerrainFormView.as_view(), name="terrain_form"),
    path('location_form', views.LocationFormView.as_view(), name="location_form"),
]
