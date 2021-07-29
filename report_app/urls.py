from django.urls import path
from . import views

urlpatterns = [
    path('forward', views.forward),
    path('backward', views.backward),
    path('rep_rcv', views.report_receiving),
    path('rep_shp', views.report_shipped),
    path('edit', views.edit),
    path('receiving/<int:doc_id>', views.edit_receiving),
    path('shipping/<int:doc_id>', views.edit_shipping),
    path('incoming/<int:doc_id>', views.edit_incoming),
    path('finished/<int:doc_id>', views.edit_finished),
    path('rep_inc', views.report_incoming),
    path('rep_fin', views.report_finished),
]
