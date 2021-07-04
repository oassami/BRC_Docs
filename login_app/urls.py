from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  # path('register', views.register),
  path('user/register', views.user_register),
  path('user/login', views.user_login),
  # path('clear_all', views.clear_forms),
  # path('user/pw_reset', views.pw_reset),
  # path('reseted', views.reseted),
]
