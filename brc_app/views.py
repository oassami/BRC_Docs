from django.shortcuts import render, redirect
from django.db.models import Count
from login_app.models import User
from . models import *
# from datetime import date
from django.contrib import messages
import bcrypt

def main(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  return render(request, 'main.html')

def users(request):
  if 'logged_in' not in request.session or not request.session['user_level'] == "Admin":
    return redirect('/')
  context = {
    'all_users': User.objects.all(),
  }
  return render(request, 'users_list.html', context)

def user_add(request):
  if 'logged_in' not in request.session:
      return redirect('/')
  if request.method == "GET":
    return render(request, 'user_add_edit.html')
  else:
    if not request.session['user_level'] == "Admin":
      return redirect('/')
    errors = User.objects.addValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/brc/user/add')
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
        level = request.POST['level'],
    )
  return redirect('/brc/users')

def user_edit(request, user_id):
  if 'logged_in' not in request.session or not request.session['user_level'] == "Admin":
    return redirect('/')
  user = User.objects.get(id=user_id)
  if request.method == 'GET':
    context={
      'this_user': user,
      'edit': True
    }
    return render(request, 'user_add_edit.html', context)
  else:
    errors = User.objects.editValidation(request.POST, user)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f'/brc/user/edit/{user.id}')
    if request.POST['first_name']:
      user.first_name = request.POST['first_name']
      if user.id == request.session['user_id']:
        request.session['first_name'] = request.POST['first_name']
    if request.POST['last_name']:
      user.last_name = request.POST['last_name']
      if user.id == request.session['user_id']:
        request.session['last_name'] = request.POST['last_name']
    if request.POST['email']:
      user.email = request.POST['email']
      if user.id == request.session['user_id']:
        request.session['email'] = request.POST['email']
    if request.POST['password']:
      user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user.level = request.POST['level']
    if user.id == request.session['user_id']:
      request.session['user_level'] = request.POST['level']
    user.save()
    if user.id == request.session['user_id']:
      return redirect('/brc')
  return redirect('/brc/users')

def user_delete(request, user_id):
  if 'logged_in' in request.session and user_id != request.session['user_id'] and request.session['user_level'] == "Admin":
    try:
      user = User.objects.get(id=user_id)
      user.delete()
    except:
      pass
  else:
    return redirect('/')
  return redirect('/brc/users')

def employees(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  context = {
    'all_employees': Employee.objects.all().order_by('-active', 'emp_id'),
  }
  return render(request, 'employees_list.html', context)

def employee_add(request):
  if 'logged_in' not in request.session:
      return redirect('/')
  if request.method == "GET":
    return render(request, 'employee_add_edit.html')
  else:
    errors = Employee.objects.empAddValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/brc/employee/add')
    employee = Employee.objects.create(
        emp_id = request.POST['emp_id'],
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        level = request.POST['level'],
        active = True,
    )
  return redirect('/brc/employee')

def employee_edit(request, emp_id):
  if 'logged_in' not in request.session:
    return redirect('/')
  emp = Employee.objects.get(id=emp_id)
  if request.method == 'GET':
    context={
      'this_employee': emp,
      'edit': True
    }
    return render(request, 'employee_add_edit.html', context)
  else:
    errors = Employee.objects.empEditValidation(request.POST, emp)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f'/brc/employee/edit/{emp.id}')
    if request.POST['emp_id']:
      emp.emp_id = request.POST['emp_id']
    if request.POST['first_name']:
      emp.first_name = request.POST['first_name']
    if request.POST['last_name']:
      emp.last_name = request.POST['last_name']
    emp.level = request.POST['level']
    emp.save()
  return redirect('/brc/employee')

def employee_inactive(request, emp_id):
  if 'logged_in' in request.session:
    try:
      emp = Employee.objects.get(id=emp_id)
      if emp.active:
        emp.active = False
      else:
        emp.active = True
      emp.save()
    except:
      pass
  else:
    return redirect('/')
  return redirect('/brc/employee')

def others(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  request.session['other_name'] = ''
  request.session['other_address'] = ''
  request.session['other_city'] = ''
  request.session['other_state'] = ''
  request.session['other_zipcode'] = ''
  request.session['other_phone'] = ''
  if request.path == '/brc/customer':
    context = {
      'all_others': Customer.objects.all().order_by('-active'),
      'source': 'Customer',
      'path': 'customer',
    }
  elif request.path == '/brc/supplier':
    context = {
      'all_others': Supplier.objects.all().order_by('-active'),
      'source': 'Supplier',
      'path': 'supplier',
    }
  elif request.path == '/brc/trucking':
    context = {
      'all_others': Truck.objects.all().order_by('-active'),
      'source': 'Truck',
      'path': 'trucking',
    }
  else:
    context = {}
  return render(request, 'others_list.html', context)

def other_add(request):
  if 'logged_in' not in request.session:
      return redirect('/')
  if request.method == "GET":
    if request.path == '/brc/customer/add':
      context = {
        'source': 'Customer',
        'path': 'customer',
        'edit': False
      }
    elif request.path == '/brc/supplier/add':
      context = {
        'source': 'Supplier',
        'path': 'supplier',
        'edit': False
      }
    elif request.path == '/brc/trucking/add':
      context = {
        'source': 'Truck',
        'path': 'trucking',
        'edit': False
      }
    else:
      context={}
    return render(request, 'other_add_edit.html', context)
  else:
    request.session['other_name'] = request.POST['name']
    request.session['other_address'] = request.POST['address']
    request.session['other_city'] = request.POST['city']
    request.session['other_state'] = request.POST['state']
    request.session['other_zipcode'] = request.POST['zipcode']
    request.session['other_phone'] = request.POST['phone']
    if '/brc/customer/add' in request.path:
      errors = Customer.objects.addValidation(request.POST)
      if errors:
        for key, value in errors.items():
          messages.error(request, value)
        return redirect('/brc/customer/add')
      Customer.objects.create(
          name = request.POST['name'],
          address = request.POST['address'],
          city = request.POST['city'],
          state = request.POST['state'],
          zipcode = request.POST['zipcode'],
          phone = request.POST['phone'],
          active = True)
      return redirect('/brc/customer')
    elif '/brc/supplier/add' in request.path:
      errors = Supplier.objects.addValidation(request.POST)
      if errors:
        for key, value in errors.items():
          messages.error(request, value)
        return redirect('/brc/supplier/add')
      Supplier.objects.create(
          name = request.POST['name'],
          address = request.POST['address'],
          city = request.POST['city'],
          state = request.POST['state'],
          zipcode = request.POST['zipcode'],
          phone = request.POST['phone'],
          active = True)
      return redirect('/brc/supplier')
    else:
      errors = Truck.objects.addValidation(request.POST)
      if errors:
        for key, value in errors.items():
          messages.error(request, value)
        return redirect('/brc/trucking/add')
      Truck.objects.create(
          name = request.POST['name'],
          address = request.POST['address'],
          city = request.POST['city'],
          state = request.POST['state'],
          zipcode = request.POST['zipcode'],
          phone = request.POST['phone'],
          active = True)
      return redirect('/brc/trucking')

def other_edit(request, other_id):
  if 'logged_in' not in request.session:
    return redirect('/')
  if request.method == 'GET':
    if '/brc/customer/edit' in request.path:
      context = {
        'this_other': Customer.objects.get(id=other_id),
        'source': 'Customer',
        'path': 'customer',
        'edit': True
      }
    elif '/brc/supplier/edit' in request.path:
      context = {
        'this_other': Supplier.objects.get(id=other_id),
        'source': 'Supplier',
        'path': 'supplier',
        'edit': True
      }
    elif '/brc/trucking/edit' in request.path:
      context = {
        'this_other': Truck.objects.get(id=other_id),
        'source': 'Trucking',
        'path': 'trucking',
        'edit': True
      }
    else:
      context={}
    request.session['other_name'] = context['this_other'].name
    request.session['other_address'] = context['this_other'].address
    request.session['other_city'] = context['this_other'].city
    request.session['other_state'] = context['this_other'].state
    request.session['other_zipcode'] = context['this_other'].zipcode
    request.session['other_phone'] = context['this_other'].phone
    return render(request, 'other_add_edit.html', context)
  else:
    if '/brc/customer/edit' in request.path:
      other = Customer.objects.get(id=other_id)
      errors = Customer.objects.editValidation(request.POST, other)
      path = "customer"
    elif '/brc/supplier/edit' in request.path:
      other = Supplier.objects.get(id=other_id)
      errors = Supplier.objects.editValidation(request.POST, other)
      path = "supplier"
    else:
      other = Truck.objects.get(id=other_id)
      errors = Truck.objects.editValidation(request.POST, other)
      path = "trucking"
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f'/brc/{path}/edit/{other.id}')
    if request.POST['name']:
      other.name = request.POST['name']
    if request.POST['address']:
      other.address = request.POST['address']
    if request.POST['city']:
      other.city = request.POST['city']
    if request.POST['state']:
      other.state = request.POST['state']
    if request.POST['zipcode']:
      other.zipcode = request.POST['zipcode']
    if request.POST['phone']:
      other.phone = request.POST['phone']
    other.save()
  return redirect(f'/brc/{path}')

def other_inactive(request, other_id):
  if 'logged_in' in request.session:
    try:
      if '/brc/customer/inactive' in request.path:
        other = Customer.objects.get(id=other_id)
        path = "customer"
      elif '/brc/supplier/inactive' in request.path:
        other = Supplier.objects.get(id=other_id)
        path = "supplier"
      else:
        other = Truck.objects.get(id=other_id)
        path = "trucking"
      if other.active:
        other.active = False
      else:
        other.active = True
      other.save()
    except:
      pass
  else:
    return redirect('/')
  return redirect(f'/brc/{path}')

def receiving(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  request.session['date'] = ''
  request.session['product'] = ''
  request.session['lot'] = ''
  request.session['qty'] = ''
  request.session['best_by'] = ''
  request.session['supplier'] = ''
  request.session['truck'] = ''
  request.session['truck_no'] = ''
  request.session['employee'] = ''
  if request.path == '/brc/receiving':
    # rcv = Receive.objects.all().order_by('receive_date')
    # for x in rcv:
      # print(rcv)
      # print('xxx', x.receive_date)
      # print('yyy', x.product.prod_name)
      # print('zzz', x.product.lot_num)
      # print('aaa', x.product.best_by)
      # print('sss', x.employee.first_name)
    context = {
      'others': Receive.objects.all().order_by('receive_date'),
      'source': 'Receiving',
      'path': 'receiving',
    }
  else:
    context = {}
  return render(request, 'rcv_shp_list.html', context)

def receiving_add(request):
  if 'logged_in' not in request.session:
      return redirect('/')
  if request.method == "GET":
    if request.path == '/brc/receiving/add':
      context = {
        'suppliers': Supplier.objects.all().exclude(active=False),
        'trucks': Truck.objects.all().exclude(active=False),
        'employees': Employee.objects.all().exclude(active=False),
        'source': 'Receiving',
        'path': 'receiving',
        'edit': False
      }
    else:
      context={}
    return render(request, 'rcv_shp_add_edit.html', context)
  else:
    request.session['date'] = request.POST['date']
    request.session['product'] = request.POST['product']
    request.session['lot'] = request.POST['lot']
    request.session['qty'] = request.POST['qty']
    request.session['best_by'] = request.POST['best_by']
    request.session['supplier'] = request.POST['supplier']
    request.session['truck'] = request.POST['truck']
    request.session['truck_no'] = request.POST['truck_no']
    request.session['employee'] = request.POST['employee']
    if '/brc/receiving/add' in request.path:
      errors = Receive.objects.addRcValidation(request.POST)
      if errors:
        for key, value in errors.items():
          messages.error(request, value)
        return redirect('/brc/receiving/add')
      this_product = Product.objects.create(
        lot_num = request.POST['lot'],
        prod_name = request.POST['product'],
        best_by = request.POST['best_by'],
        type = "I")
      this_supplier = Supplier.objects.get(id=request.POST['supplier'])
      this_truck = Truck.objects.get(id=request.POST['truck'])
      this_employee = Employee.objects.get(id=request.POST['employee'])
      Receive.objects.create(
        receive_date = request.POST['date'],
        product = this_product,
        qty = request.POST['qty'],
        supplier = this_supplier,
        trucker = this_truck,
        employee = this_employee)
      return redirect('/brc/receiving')
    else:
      return redirect('/brc/shipping')

def production(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  request.session['pdate'] = ''
  request.session['ilot1'] = ''
  request.session['iname1'] = ''
  request.session['iqty1'] = ''
  request.session['ilot2'] = ''
  request.session['iname2'] = ''
  request.session['iqty2'] = ''
  request.session['flot'] =''
  request.session['fname'] =''
  request.session['fqty'] = ''
  request.session['fbbdate'] = ''
  request.session['pemp1'] = ''
  request.session['pemp2'] = ''
  request.session['pemp3'] = ''
  request.session['pemp4'] = ''
  request.session['pemp5'] = ''
  request.session['pemp6'] = ''
  request.session['pemp7'] = ''
  request.session['pemp8'] = ''
  request.session['pemp9'] = ''
  request.session['liner'] = ''
  request.session['tubs'] = ''
  request.session['lids'] = ''
  request.session['remployee'] = ''
  request.session['rdate'] = ''
  productions = Production.objects.all().order_by('production_date')
  products = ProdProduct.objects.all()
  # for prod in products:
    # print(prod.incoong)
  
  for production in productions:
    print(production.products.all())
    for product in products.filter(type='F'):
      print('y')
      # fid = production_product.id
      print(product.prod_name)
      print(product.lot_num)
      print(product.type)

  context = {
    'productions': productions,
    'products': production.incoming_products.all(),
    'add': False,
  }
  return render(request, 'production.html', context)

def production_add(request):
  if 'logged_in' not in request.session:
      return redirect('/')
  if request.method == "GET":
    context = {
      'ilots': Product.objects.filter(type="I"), # .exclude(active=False),
      'employees': Employee.objects.all().exclude(active=False),
      'add': True,
    }
    return render(request, 'production.html', context)
  else:
    request.session['pdate'] = request.POST['pdate']
    request.session['ilot1'] = request.POST['ilot1']
    request.session['iname1'] = request.POST['iname1']
    request.session['iqty1'] = request.POST['iqty1']
    request.session['ilot2'] = request.POST['ilot2']
    request.session['iname2'] = request.POST['iname2']
    request.session['iqty2'] = request.POST['iqty2']
    request.session['flot'] = request.POST['flot']
    request.session['fname'] = request.POST['fname']
    request.session['fqty'] = request.POST['fqty']
    request.session['fbbdate'] = request.POST['fbbdate']
    request.session['pemp1'] = request.POST['pemp1']
    request.session['pemp2'] = request.POST['pemp2']
    request.session['pemp3'] = request.POST['pemp3']
    request.session['pemp4'] = request.POST['pemp4']
    request.session['pemp5'] = request.POST['pemp5']
    request.session['pemp6'] = request.POST['pemp6']
    request.session['pemp7'] = request.POST['pemp7']
    request.session['pemp8'] = request.POST['pemp8']
    request.session['pemp9'] = request.POST['pemp9']
    request.session['liner'] = request.POST['liner']
    request.session['tubs'] = request.POST['tubs']
    request.session['lids'] = request.POST['lids']
    request.session['remployee'] = request.POST['remployee']
    request.session['rdate'] = request.POST['rdate']
    # if '/brc/receiving/add' in request.path:
    errors = Production.objects.addProValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/brc/production/add')
    fproduct = Product.objects.create(
      lot_num = request.POST['flot'],
      prod_name = request.POST['fname'],
      best_by = request.POST['fbbdate'],
      type = "F")
    this_production = Production.objects.create(
      production_date = request.POST['pdate'],
      liner = request.POST['liner'],
      tubs = request.POST['tubs'],
      lids = request.POST['lids'],
      released_by = Employee.objects.get(id=request.POST['remployee']),
      released_date = request.POST['rdate'])
    iproduct = Product.objects.get(id=request.POST['ilot1'])
    this_production.products.add(iproduct)
    this_production.products.add(fproduct)
    ProdProduct.objects.create(
      productions = this_production,
      products = iproduct,
      qtys = request.POST['iqty1'])
    ProdProduct.objects.create(
      productions = this_production,
      products = fproduct,
      qtys = request.POST['fqty'])
    if request.POST['ilot2'] != '9999' and request.POST['ilot2'] != '0':
      iproduct = Product.objects.get(id=request.POST['ilot2'])
      this_production.products.add(iproduct)
      ProdProduct.objects.create(
        productions = this_production,
        products = iproduct,
        qtys = request.POST['iqty2'])
    prod_locations = ['Push-In/Collect', 'Case/Cardboard', 'Box Open/Dumper', 'Metal Detector', 'Taping', 'Labeling', 'Sort Conveyor', 'Sort Conveyor', 'Sort Conveyor']
    for i in range(1, 9+1):
      # print(request.POST[f'pemp{i}'])
      if request.POST[f'pemp{i}'] != '9999':
        this_employee = Employee.objects.get(id=request.POST[f'pemp{i}'])
        this_production.employees.add(this_employee)
        ProdEmployee.objects.create(
          productions = this_production,
          employees = this_employee,
          locations = prod_locations[i-1])
    return redirect('/brc/production')
