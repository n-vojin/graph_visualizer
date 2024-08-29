from django.urls import path
from . import views

urlpatterns = [
    # path(),
    path('', views.index, name='index'),
    path('loader/<str:loader_id>', views.index, name='loader_plugin'),
]
