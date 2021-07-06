from django.db import models
from login_app.models import User

class InfoManager(models.Manager):
  def empAddValidation(self, post_data):
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
  
  def empEditValidation(self, post_data, emp):
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

  def addValidation(self, post_data):
    errors={}
    if len(post_data['name']) < 2:
      errors['name'] = 'Name must be at least 2 characters.'
    if len(post_data['address']) < 2:
      errors['address'] = 'Address must be at least 2 characters.'
    if len(post_data['city']) < 2:
      errors['city'] = 'City must be at least 2 characters.'
    if len(post_data['state']) != 2:
      errors['state'] = 'State must be 2 characters.'
    if len(post_data['zipcode']) < 5:
      errors['zipcode'] = 'Zip Code must be at least 5 characters.'
    if len(post_data['phone']) < 10:
      errors['phone'] = 'Phone # must be at least 10 characters.'
    try:
      self.get(phone=post_data['phone'])
      errors['phone'] = "This Phone Number already exists!"
    except:
      pass
    return errors
  
  def editValidation(self, post_data, other):
    errors={}
    if len(post_data['name']) < 2:
      errors['name'] = 'Name must be at least 2 characters.'
    if len(post_data['address']) < 2:
      errors['address'] = 'Address must be at least 2 characters.'
    if len(post_data['city']) < 2:
      errors['city'] = 'City must be at least 2 characters.'
    if len(post_data['state']) != 2:
      errors['state'] = 'State must be 2 characters.'
    if len(post_data['zipcode']) < 5:
      errors['zipcode'] = 'Zip Code must be at least 5 characters.'
    if len(post_data['phone']) < 10:
      errors['phone'] = 'Phone # must be at least 10 characters.'
    if other.phone != post_data['phone']:
      try:
        self.get(phone=post_data['phone'])
        errors['phone'] = "This Phone Number already exists!"
      except:
        pass
    return errors

class Employee(models.Model):
  emp_id= models.CharField(max_length=10, unique=True)
  first_name = models.CharField(max_length=55)
  last_name = models.CharField(max_length=55)
  level = models.CharField(max_length=10)
  active = models.BooleanField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class Customer(models.Model):
  name = models.CharField(max_length=55)
  address = models.CharField(max_length=55)
  city = models.CharField(max_length=55)
  state = models.CharField(max_length=2)
  zipcode = models.CharField(max_length=10)
  phone = models.CharField(max_length=10)
  active = models.BooleanField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class Supplier(models.Model):
  name = models.CharField(max_length=55)
  address = models.CharField(max_length=55)
  city = models.CharField(max_length=55)
  state = models.CharField(max_length=2)
  zipcode = models.CharField(max_length=10)
  phone = models.CharField(max_length=10)
  active = models.BooleanField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class Truck(models.Model):
  name = models.CharField(max_length=55)
  address = models.CharField(max_length=55)
  city = models.CharField(max_length=55)
  state = models.CharField(max_length=2)
  zipcode = models.CharField(max_length=10)
  phone = models.CharField(max_length=10)
  active = models.BooleanField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()
