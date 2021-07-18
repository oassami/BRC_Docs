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
    if post_data['supp_cust'] == '0':
      errors['supp_cust'] = 'Must select a Supplier.'
    if post_data['truck'] == '0':
      errors['truck'] = 'Must select a Trucking Company.'
    if len(post_data['truck_no']) < 2:
      errors['truck_no'] = 'Truck Number must be at least 2 characters.'
    if post_data['employee'] == '0':
      errors['employee'] = 'Must select an Employee.'
    try:
      Product.objects.get(lot_num=post_data['lot'])
      errors['lot'] = "This Lot Number already exists!"
    except:
      pass
    return errors

  def addShValidation(self, post_data):
    errors={}
    if not post_data['date']:
      errors['date'] = 'Invalid date...'
    # if len(post_data['product']) < 2:
      # errors['product'] = 'Product must be at least 2 characters.'
    if post_data['lot'] == '0':
      errors['lot'] = 'Must select a LOT Number'
    if not post_data['qty']:
      errors['qty'] = 'Quantity connot be less than 1.'
    # if not post_data['best_by']:
    #   errors['best_by'] = 'Invalid Best By date...'
    if post_data['supp_cust'] == '0':
      errors['supp_cust'] = 'Must select a Customer.'
    if post_data['truck'] == '0':
      errors['truck'] = 'Must select a Trucking Company.'
    if len(post_data['truck_no']) < 2:
      errors['truck_no'] = 'Truck Number must be at least 2 characters.'
    if post_data['employee'] == '0':
      errors['employee'] = 'Must select an Employee.'
    # try:
    #   Product.objects.get(lot_num=post_data['lot'])
    #   errors['lot'] = "This Lot Number already exists!"
    # except:
    #   pass
    return errors

  def addProValidation(self, post_data):
    errors={}
    if not post_data['pdate']:
      errors['pdate'] = 'Invalid Production Date...'
    if post_data['ilot1'] == '0':
      errors['ilot1'] = 'Must select an Incoming Product LOT #.'
    if not post_data['iqty1']:
      errors['iqty1'] = 'Incoming Product Quantity connot be less than 1.'
    if not post_data['flot']:
      errors['flot'] = 'Must select a Finished LOT #.'
    if len(post_data['fname']) < 2:
      errors['fname'] = 'Finished Product must be at least 2 characters.'
    if not post_data['fqty']:
      errors['fqty'] = 'Finished Product Quantity connot be less than 1.'
    if not post_data['fbbdate']:
      errors['fbbdate'] = 'Invalid Best By Date...'
    if post_data['pemp1'] == '0' or post_data['pemp2'] == '0' or post_data['pemp3'] == '0'  or post_data['pemp4'] == '0' or post_data['pemp5'] == '0' or post_data['pemp6'] == '0' or post_data['pemp7'] == '0' or post_data['pemp8'] == '0' or post_data['pemp9'] == '0':
      errors['pemp'] = 'Must select all Poduction Employee (or NONE).'
    if len(post_data['liner']) < 2:
      errors['liner'] = 'Liner LOT # must be at least 2 characters.'
    if len(post_data['tubs']) < 2:
      errors['tubs'] = 'Tubs LOT # must be at least 2 characters.'
    if len(post_data['lids']) < 2:
      errors['lids'] = 'Lids LOT # must be at least 2 characters.'
    if post_data['remployee'] == '0':
      errors['remployee'] = 'Must select Release Employee.'
    if not post_data['rdate']:
      errors['rdate'] = 'Invalid Release Date...'
    try:
      Product.objects.get(lot_num=post_data['flot'])
      errors['flot'] = "Finished Product Lot # already exists!"
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

class Product(models.Model):
  lot_num = models.CharField(max_length=55)
  prod_name = models.CharField(max_length=55)
  best_by = models.DateField()
  type = models.CharField(max_length=1) # "I" for Incoming, "F" for Finished
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

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

class Receive(models.Model):
  receive_date = models.DateField()
  product = models.ForeignKey(Product, related_name='received_product', on_delete=models.CASCADE)
  qty = models.IntegerField()
  supplier = models.ForeignKey(Supplier, related_name='suppliers', on_delete=models.CASCADE)
  trucker = models.ForeignKey(Truck, related_name='received_truckers', on_delete=models.CASCADE)
  employee = models.ForeignKey(Employee, related_name='recieved_by', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class Ship(models.Model):
  ship_date = models.DateField()
  product = models.ForeignKey(Product, related_name='shipped_product', on_delete=models.CASCADE)
  qty = models.IntegerField()
  customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE)
  trucker = models.ForeignKey(Truck, related_name='shipped_truckers', on_delete=models.CASCADE)
  employee = models.ForeignKey(Employee, related_name='shipped_by', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class Production(models.Model):
  production_date = models.DateField()
  created_by = models.ForeignKey(User, related_name='procductions_user', on_delete=models.CASCADE)
  liner_lot = models.CharField(max_length=55)
  tubs_lot = models.CharField(max_length=55)
  lids_lot = models.CharField(max_length=55)
  released_by = models.ForeignKey(Employee, related_name='productions', on_delete=models.CASCADE)
  released_date = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = InfoManager()

class ProdProduct(models.Model):
  production = models.ForeignKey(Production, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class ProdEmployee(models.Model):
  production = models.ForeignKey(Production, on_delete=models.CASCADE)
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
  location = models.CharField(max_length=10)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
