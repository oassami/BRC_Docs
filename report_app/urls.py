from django.urls import path
from . import views

urlpatterns = [
    path('forward', views.forward),
    path('backward', views.backward),
    path('rep_rcv', views.report_receiving),
    path('rep_shp', views.report_shipped),
    path('edit', views.edit_docs),
    path('rep_inc', views.report_incoming),
    path('rep_fin', views.report_finished),
]
