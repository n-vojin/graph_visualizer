from django.apps.registry import apps
from django.shortcuts import render, redirect



def index(request):
    return render(request, 'index.html')

#def ucitavanje_plugin(request, id):
#    return render()
#........