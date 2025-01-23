from django.urls import path
from . import views

urlpatterns = [
     path('', views.graphPage_view),
     path('graph', views.graphPage_view),
     path('load_graph', views.load_graph_view),
     path('upload_data', views.upload_data_view),
     path('load_graph_tables', views.load_graph_tables_view),
     path('update_data_from_process_tables', views.update_data_from_process_tables_view),
     path('preditct_data_from_process_tables', views.preditct_data_from_process_tables_view)
     
     
]