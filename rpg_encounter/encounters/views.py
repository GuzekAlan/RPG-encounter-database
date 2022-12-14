from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from rpg_encounter.utils import executeScriptsFromFile
from os import path

# Create your views here.
def index(request):
    cursor = connection.cursor()
    executeScriptsFromFile(path.join(path.dirname(__file__), 'sql/DDL.sql'), cursor=cursor)
    return HttpResponse("Welcome to RPG Encounter Database")

def database(request):
    return HttpResponse("Your request: " + request)