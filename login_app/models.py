from django.db import models
from datetime import date, time, datetime, timedelta
import re, bcrypt

class UserManager(models.Manager):
  def addValidation(self, post_data):
      errors={}
      email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      if len(post_data['first_name']) < 2:
          errors['first_name'] = 'First name must be at least 2 characters'
      if len(post_data['last_name']) < 2:
          errors['last_name'] = 'Last name must be at least 2 characters'
      if not email_regex.match(post_data['email']):
          errors['email'] = "Invalid email address!"
      else:
          try:
              self.get(email=post_data['email'])                  # try and get the record from database
              errors['email'] = "This email already exists!"      # it found one record in database
          except:
              pass                                                # did not find a record which what we need, so, do nothing and continue
      if len(post_data['password']) < 8:
          errors['password'] = 'Password must be at least 8 characters'
      else:
          if post_data['password'] != post_data['c_password']:
              errors['password'] = 'Passwords do not match!'
      return errors

  def loginValidation(self, post_data):
      errors = {}
      email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      if not post_data['password']:
          errors['password'] = 'Password is missing!'
      if not email_regex.match(post_data['email']):
          errors['email'] = "Invalid email address!"
      return errors

  def resetValidation(self, post_data):
      errors = {}
      email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      if not post_data['password']:
          errors['password'] = 'Password is missing!'
      if not email_regex.match(post_data['email']):
          errors['email'] = "Invalid email address!"
      if len(post_data['password']) < 8:
          errors['password'] = 'Password must be at least 8 characters'
      else:
          if post_data['password'] != post_data['c_password']:
              errors['password'] = 'Passwords do not match!'
      return errors

  def editValidation(self, post_data, user):
    errors = {}
    print(post_data['level'])
    print(user.level)
    if post_data['level'] == "Normal" and user.level == "Admin":
      admins = self.filter(level="Admin")
      if admins.count() < 2:
        errors['level1'] = "You are the only Administrator in the database..."
        errors['level2'] = "You need to give someone else that status before changing yours!"
    if post_data['first_name']:
      if len(post_data['first_name']) < 1:
        errors['first_name'] = 'First name must be at least 1 characters'
    if post_data['last_name']:
      if len(post_data['last_name']) < 1:
        errors['last_name'] = 'Last name must be at least 1 characters'
    if post_data['email']:
      email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      if not email_regex.match(post_data['email']):
        errors['email'] = "Invalid email address!"
      else:
        if post_data['email'] != user.email:
          try:
            self.get(email=post_data['email'])
            errors['email'] = "This email already exists!"
          except:
            pass
        if post_data['password']:
          if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
          else:
            if post_data['password'] != post_data['c_password']:
              errors['password'] = 'Passwords do not match!'
    return errors

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    level = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
