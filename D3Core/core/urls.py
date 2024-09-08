from django.urls import path
from . import views

urlpatterns = [
    # path(),
    path('', views.index, name='index'),
    path('loader/<str:loader_id>', views.index, name='loader_plugin'),
    path('visualizer/<str:loader_id>', views.index, name='visualizer_plugin'),

    path('get_graph_data/', views.get_graph_data, name='get_graph_data'),
    path('fetch_graph_data/', views.fetch_graph_data, name='fetch_graph_data'),
    path('visualise/', views.visualise, name='visualise'),
]
