from django.urls import path
from . import views

urlpatterns = [
    path('forward', views.forward),
    path('backward', views.backward),
]
