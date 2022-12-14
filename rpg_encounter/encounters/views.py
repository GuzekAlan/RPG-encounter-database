from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from rpg_encounter.utils import executeScriptsFromFile
from os import path


def index(request):
    return HttpResponse("<h1>Welcome to RPG Encounter Database</h1>")

def create_database(request):
    with connection.cursor() as cursor:
        executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DDL.sql'), cursor=cursor)
    return HttpResponse("Database structure created!")

def database(request):
    return HttpResponse("Your request: " + request)