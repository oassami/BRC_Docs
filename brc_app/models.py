from django.db import models
from login_app.models import User

class InfoManager(models.Manager):
  def addValidation(self, post_data):
    errors={}
    # print('f ', post_data['first_name'])
    # print('l ', post_data['last_name'])

    if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
      errors[''] = 'First / Last Name must be at least 2 characters.'
    return errors

class Employee(models.Model):
  first_name = models.CharField(max_length=55)
  last_name = models.CharField(max_length=55)
  # email = models.EmailField(unique=True)
  # password = models.CharField(max_length=128)
  level = models.CharField(max_length=10)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()
