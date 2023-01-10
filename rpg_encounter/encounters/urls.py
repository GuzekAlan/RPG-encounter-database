from django.urls import path
from rpg_encounter.encounters import views

app_name = 'encounters'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('create_database', views.CreateDatabaseView.as_view(), name="create_database"),
    path('terrain_form', views.TerrainFormView.as_view(), name="terrain_form"),
    path('location_form', views.LocationFormView.as_view(), name="location_form"),
    path('treasure_form', views.TreasureFormView.as_view(), name="treasure_form"),
    path('race_form', views.RaceFormView.as_view(), name="race_form"),
    path('monster_form', views.MonsterFormView.as_view(), name="monster_form"),
    path('trap_form', views.TrapFormView.as_view(), name="trap_form"),
    path('encounter_form', views.EncounterFormView.as_view(), name="encounter_form"),
    path('terrain_table', views.TerrainTableView.as_view(), name="terrain_table"),
    path('location_table', views.LocationTableView.as_view(), name="location_table"),
    path('treasure_table', views.TreasureTableView.as_view(), name="treasure_table"),
    path('race_table', views.RaceTableView.as_view(), name="race_table"),
    path('monster_table', views.MonsterTableView.as_view(), name="monster_table"),
    path('trap_table', views.TrapTableView.as_view(), name="trap_table"),
    path('encounter_table', views.EncounterTableView.as_view(), name="encounter_table"),
]
