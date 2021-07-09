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

  def addRcValidation(self, post_data):
    errors={}
    if not post_data['date']:
      errors['date'] = 'Invalid date...'
    if len(post_data['product']) < 2:
      errors['product'] = 'Product must be at least 2 characters.'
    if len(post_data['lot']) < 2:
      errors['lot'] = 'Lot Number must be at least 2 characters.'
    if not post_data['qty']:
      errors['qty'] = 'Quantity connot be less than 1.'
    if not post_data['best_by']:
      errors['best_by'] = 'Invalid Best By date...'
    if post_data['supplier'] == '0':
      errors['supplier'] = 'Must select a Supplier.'
    if post_data['truck'] == '0':
      errors['truck'] = 'Must select a Trucking Company.'
    if len(post_data['truck_no']) < 2:
      errors['truck_no'] = 'Truck Number must be at least 2 characters.'
    if post_data['employee'] == '0':
      errors['employee'] = 'Must select an Employee.'
    try:
      Incoming.objects.get(lot_num=post_data['lot'])
      errors['lot'] = "This Lot Number already exists!"
    except:
      print('ERRORRRR!')
    return errors

  def addShValidation(self, post_data):
    errors={}
    if not post_data['date']:
      errors['date'] = 'Invalid date...'
    if len(post_data['product']) < 2:
      errors['product'] = 'Product must be at least 2 characters.'
    if len(post_data['lot']) < 2:
      errors['lot'] = 'Lot Number must be at least 2 characters.'
    if not post_data['qty']:
      errors['qty'] = 'Quantity connot be less than 1.'
    if not post_data['best_by']:
      errors['best_by'] = 'Invalid Best By date...'
    if post_data['supplier'] == '0':
      errors['supplier'] = 'Must select a Supplier.'
    if post_data['truck'] == '0':
      errors['truck'] = 'Must select a Trucking Company.'
    if len(post_data['truck_no']) < 2:
      errors['truck_no'] = 'Truck Number must be at least 2 characters.'
    if post_data['employee'] == '0':
      errors['employee'] = 'Must select an Employee.'
    try:
      Finished.objects.get(lot_num=post_data['lot'])
      errors['lot'] = "This Lot Number already exists!"
    except:
      print('ERRORRRR!')
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

class Incoming(models.Model):
  lot_num = models.CharField(max_length=55)
  prod_name = models.CharField(max_length=55)
  best_by = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Finished(models.Model):
  lot_num = models.CharField(max_length=55)
  prod_name = models.CharField(max_length=55)
  best_by = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Receive(models.Model):
  receive_date = models.DateField()
  product = models.ForeignKey(Incoming, related_name='received_product', on_delete=models.CASCADE)
  qty = models.IntegerField()
  supplier = models.ForeignKey(Supplier, related_name='suppliers', on_delete=models.CASCADE)
  trucker = models.ForeignKey(Truck, related_name='received_truckers', on_delete=models.CASCADE)
  employee = models.ForeignKey(Employee, related_name='recieved_by', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class Ship(models.Model):
  ship_date = models.DateField()
  product = models.ForeignKey(Incoming, related_name='shipped_product', on_delete=models.CASCADE)
  qty = models.IntegerField()
  customer = models.ForeignKey(Supplier, related_name='customers', on_delete=models.CASCADE)
  trucker = models.ForeignKey(Truck, related_name='shipped_truckers', on_delete=models.CASCADE)
  employee = models.ForeignKey(Employee, related_name='shipped_by', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class Production(models.Model):
  production_date = models.DateField()
  incoming1 = models.ForeignKey(Incoming, related_name='received_product1', on_delete=models.CASCADE)
  incoming1_qty = models.IntegerField()
  incoming2 = models.ForeignKey(Incoming, related_name='received_product2', on_delete=models.CASCADE)
  incoming2_qty = models.IntegerField()
  finished = models.ForeignKey(Finished, related_name='shinished_product', on_delete=models.CASCADE)
  finished_qty = models.IntegerField()
  employee = models.ManyToManyField(Employee, related_name='production_by')
  liner = models.CharField(max_length=55)
  tubs = models.CharField(max_length=55)
  lids = models.CharField(max_length=55)
  released_by = models.ForeignKey(User, related_name='productions', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()
