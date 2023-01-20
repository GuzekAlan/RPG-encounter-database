from django.urls import path
from rpg_encounter.encounters import views

app_name = "encounters"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create_database", views.CreateDatabaseView.as_view(), name="create_database"),
    path("terrain_form", views.TerrainFormView.as_view(), name="terrain_form"),
    path("location_form", views.LocationFormView.as_view(), name="location_form"),
    path("treasure_form", views.TreasureFormView.as_view(), name="treasure_form"),
    path("race_form", views.RaceFormView.as_view(), name="race_form"),
    path("monster_form", views.MonsterFormView.as_view(), name="monster_form"),
    path("trap_form", views.TrapFormView.as_view(), name="trap_form"),
    path("encounter_form", views.EncounterFormView.as_view(), name="encounter_form"),
    path("terrain_table", views.TerrainTableView.as_view(), name="terrain_table"),
    path("location_table", views.LocationTableView.as_view(), name="location_table"),
    path("treasure_table", views.TreasureTableView.as_view(), name="treasure_table"),
    path("race_table", views.RaceTableView.as_view(), name="race_table"),
    path("monster_table", views.MonsterTableView.as_view(), name="monster_table"),
    path("trap_table", views.TrapTableView.as_view(), name="trap_table"),
    path("encounter_table", views.EncounterTableView.as_view(), name="encounter_table"),
    path("register", views.UserRegisterFormView.as_view(), name="register"),
    path("login", views.UserLoginFormView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("delete_terrain", views.DeleteTerrainView.as_view(), name="delete_terrain"),
    path("delete_location", views.DeleteLocationView.as_view(), name="delete_location"),
    path("delete_treasure", views.DeleteTreasureView.as_view(), name="delete_treasure"),
    path("delete_trap", views.DeleteTrapView.as_view(), name="delete_trap"),
    path("delete_race", views.DeleteRaceView.as_view(), name="delete_race"),
    path("delete_monster", views.DeleteMonsterView.as_view(), name="delete_monster"),
    path(
        "delete_encounter", views.DeleteEncounterView.as_view(), name="delete_encounter"
    ),
]
