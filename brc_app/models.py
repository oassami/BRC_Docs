from django.db import models
from login_app.models import User

class InfoManager(models.Manager):
  def addValidation(self, post_data):
    errors={}
    if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
      errors['first_last'] = 'First / Last Name must be at least 2 characters.'
    if len(post_data['emp_id']) != 7:
      errors['emp_id'] = 'Employee ID must be 7 characters (APHxxxx).'
    try:
      self.get(emp_id=post_data['emp_id'])
      errors['emp_id'] = "This ID already exists!"
    except:
      pass
    return errors
  
  def editValidation(self, post_data, emp):
    errors={}
    if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
      errors['first_last'] = 'First / Last Name must be at least 2 characters.'
    if len(post_data['emp_id']) != 7:
      errors['emp_id'] = 'Employee ID must be 7 characters (APHxxxx).'
    if post_data['emp_id'] != emp.emp_id:
      try:
        self.get(emp_id=post_data['emp_id'])
        errors['emp_id'] = "This ID already exists!"
      except:
        pass
    return errors

class Employee(models.Model):
  emp_id= models.CharField(max_length=10, unique=True)
  first_name = models.CharField(max_length=55)
  last_name = models.CharField(max_length=55)
  level = models.CharField(max_length=10)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()
