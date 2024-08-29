from django.urls import path
from . import views

urlpatterns = [
    # path(),
    path('', views.index, name='index'),
    #path('loader/<str:loader_id>'),views.create views for this, name='loader_plugin'),
]
