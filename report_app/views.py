from django.shortcuts import render, redirect
from login_app.models import *
from brc_app.models import *
from django.contrib import messages

def forward(request):
  if 'logged_in' not in request.session:
      return redirect('/')
  if request.method == "GET":
    context = {
      'results': False,
    }
    return render(request, 'forward.html', context)
  else:
    errors = Product.objects.traceValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/reports/forward')
    this_product = Product.objects.get(lot_num=request.POST['plot'])
    if this_product.type == 'I':    # this is an incoming product
      print('1')
      received_from = Receive.objects.select_related('product', 'supplier', 'trucker', 'employee').get(product=this_product)
      try: # this incoming product was processed
        prod_iproduct = ProdProduct.objects.select_related('product', 'production').get(product=this_product)
        try_ok = True
      except: # this incoming product was NOT processed
        try_ok = False
      if try_ok: # this incoming product was processed
        prod_fproducts = ProdProduct.objects.select_related('product', 'production').filter(production=prod_iproduct.production)
        if prod_fproducts:
          print('2')
          for prod_fproduct in prod_fproducts:
            if prod_fproduct.product.type == 'F':
              print('2.1')
              shipped_to = Ship.objects.select_related('customer', 'trucker', 'employee').filter(product=prod_fproduct.product)
              qty_shipped = 0
              if shipped_to:
                print('2.2')
                for ship_to in shipped_to:
                  qty_shipped += ship_to.qty
                qty_on_hand = prod_fproduct.quantity - qty_shipped
                qty_rec_on_hand = received_from.qty-prod_iproduct.quantity
                recovered = int(100-(((prod_fproduct.quantity - (qty_shipped + qty_on_hand))/prod_fproduct.quantity)*100))
                processed_recovered = int(100-(((prod_fproduct.quantity - (qty_shipped + qty_on_hand))/prod_fproduct.quantity)*100))
                received_recovered = int(100-(((received_from.qty-(prod_iproduct.quantity + qty_rec_on_hand))/prod_iproduct.quantity)*100))
                context = {
                  'received_from': received_from,
                  'prod_iproduct': prod_iproduct,
                  'qty_rec_on_hand': qty_rec_on_hand,
                  'prod_fproduct': prod_fproduct,
                  'shipped_to': shipped_to,
                  'qty_shipped': qty_shipped,
                  'qty_on_hand': qty_on_hand,
                  'rrecovered': received_recovered,
                  'precovered': processed_recovered,
                  'product_status': 'processed_shipped',
                  'results': True,
                  'product_type': 'I'
                }
              else:
                print('2.3')
                qty_on_hand = prod_fproduct.quantity - qty_shipped
                qty_rec_on_hand = received_from.qty-prod_iproduct.quantity
                processed_recovered = int(100-(((prod_fproduct.quantity - (qty_shipped + qty_on_hand))/prod_fproduct.quantity)*100))
                received_recovered = int(100-(((received_from.qty-(prod_iproduct.quantity + qty_rec_on_hand))/prod_iproduct.quantity)*100))
                context = {
                  'received_from': received_from,
                  'prod_iproduct': prod_iproduct,
                  'qty_rec_on_hand': qty_rec_on_hand,
                  'prod_fproduct': prod_fproduct,
                  'qty_shipped': qty_shipped,
                  'qty_on_hand': qty_on_hand,
                  'rrecovered': received_recovered,
                  'precovered': processed_recovered,
                  'product_status': 'processed_not_shipped',
                  'results': True,
                  'product_type': 'I'
                  }
      else: # this incoming product was NOT processed
        print('3')
        shipped_to = Ship.objects.select_related('customer', 'trucker', 'employee').filter(product=this_product)
        qty_shipped = 0
        if shipped_to:
          print('4')
          for ship_to in shipped_to:
            qty_shipped += ship_to.qty
          qty_on_hand = received_from.qty - qty_shipped
          recovered = int(100-(((received_from.qty - (qty_shipped + qty_on_hand))/received_from.qty)*100))
          context = {
            'received_from': received_from,
            'shipped_to': shipped_to,
            'product_status': 'not_processed_shipped',
            'qty_shipped': qty_shipped,
            'qty_on_hand': qty_on_hand,
            'recovered': recovered,
            'results': True,
            'product_type': 'I'
          }
        else:
          print('5')
          context = {
            'this_product': this_product,
            'received_from': received_from,
            'product_status': 'not_processed_not_shipped',
            'results': True,
            'product_type': 'I'
          }
    else:
      print('6')
      prod_product = ProdProduct.objects.select_related('production', 'product').get(product=this_product)
      shipped_to = Ship.objects.select_related('customer', 'trucker', 'employee').filter(product=this_product)
      qty_shipped = 0
      if shipped_to:
        print('7')
        for ship_to in shipped_to:
          qty_shipped += ship_to.qty
      qty_on_hand = prod_product.quantity - qty_shipped
      recovered = int(100-(((prod_product.quantity - (qty_shipped + qty_on_hand))/prod_product.quantity)*100))
      context = {
        'prod_product': prod_product,
        'shipped_to': shipped_to,
        'qty_shipped': qty_shipped,
        'qty_on_hand': qty_on_hand,
        'recovered': recovered,
        'results': True,
        'product_type': 'F'
      }
  return render(request, 'forward.html', context)

def backward(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  if request.method == "GET":
    context = {
      'results': False,
    }
    return render(request, 'backward.html', context)
  else:
    errors = Product.objects.traceValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/reports/backward')
    this_product = Product.objects.get(lot_num=request.POST['plot'])
    if this_product.type == 'I':    # this is an incoming product
      print('1')
      recieved_from = Receive.objects.select_related('supplier', 'trucker', 'employee').get(product=this_product)
      context = {
        'this_product': this_product,
        'recieved_from': recieved_from,
        'results': True,
        'product_type': 'F'
      }
    else:
      print('2')
      prod_fproduct = ProdProduct.objects.select_related('product', 'production').get(product=this_product)
      print(prod_fproduct.product.lot_num)
      prod_products = ProdProduct.objects.select_related('product', 'production').filter(production=prod_fproduct.production)
      if prod_products.count() == 2:
        print('3')
        for p in prod_products:
          if p.product.type == 'I':
            prod_iproduct = p
        print('3.1', p.id, p.product.lot_num)
        print('3.2', prod_iproduct.product.lot_num)
        recieved_from = Receive.objects.select_related('supplier', 'trucker', 'employee').get(product=prod_iproduct.product)
        context = {
          'this_product': this_product,
          'prod_iproduct': prod_iproduct,
          'prod_fproduct': prod_fproduct,
          'recieved_from': recieved_from,
          'iprod': 1,
          'results': True,
          'product_type': 'F'
        }
      else:
        print('4')
        x = 0
        context={}
        for p in prod_products:
          if p.product.type == 'I':
            print('5', p.product.lot_num)
            x += 1
            context[f'prod_iproduct{x}'] = p
            context[f'recieved_from{x}'] = Receive.objects.select_related('supplier', 'trucker', 'employee').get(product=p.product)
        print('x',x)
        context['prod_fproduct'] = prod_fproduct
        context['this_product'] = this_product
        context['iprod'] = x
        context['results'] = True
        context['product_type'] = 'F'
  return render(request, 'backward.html', context)

def report_receiving(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  context = {
    'receives': Receive.objects.all().order_by('-receive_date'),
    'source': 'Receiving',
    'path': 'receiving',
  }
  return render(request, 'recv_report.html', context)

def report_shipped(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  context = {
    'ships': Ship.objects.all().order_by('-ship_date'),
    'source': 'Shipping',
    'path': 'shipping',
  }
  return render(request, 'ship_report.html', context)

def report_incoming(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  context = {
    'products': Product.objects.filter(type='I').order_by('-received__receive_date'),
    'source': 'Incoming Product',
    'path': 'incoming',
  }
  return render(request, 'product_report.html', context)

def report_finished(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  context = {
    'products': Product.objects.filter(type='F').order_by('-prod_produceds__production__production_date'),
    'source': 'Finished Product',
    'path': 'finished',
  }
  return render(request, 'product_report.html', context)

def edit(request):
  if 'logged_in' not in request.session or not request.session['user_level'] == "Admin":
    return redirect('/')
  if request.method == "GET":
    context = {
      'source': 'Edit',
      'results': False,
    }
    return render(request, 'edit.html', context)
  else:
    errors = Product.objects.edit_docValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/reports/edit')
    if request.POST['btnradio'] == '1': # Receiving
      context = {
        'general': Receive.objects.all().order_by('-receive_date').filter(receive_date=request.POST['doc_date']),
        'source': 'Receiving',
        'path': 'receiving',
        'results': True,
      }
    if request.POST['btnradio'] == '2': # Shipping
      context = {
        'general': Ship.objects.all().order_by('-ship_date').filter(ship_date=request.POST['doc_date']),
        # 'general': Ship.objects.all().order_by('-ship_date'),
        'source': 'Shipping',
        'path': 'shipping',
        'results': True,
      }
    if request.POST['btnradio'] == '3': # Incoming Product
      context = {
        'general': Product.objects.filter(type='I').filter(received__receive_date=request.POST['doc_date']),
        'source': 'Incoming',
        'path': 'incoming',
        'results': True,
      }
    if request.POST['btnradio'] == '4': # Finished Product
      context = {
        'general': Product.objects.filter(type='F').filter(prod_produceds__production__production_date=request.POST['doc_date']),
        'source': 'Finished',
        'path': 'finished',
        'results': True,
      }
  return render(request, 'edit.html', context)

def edit_receiving(request, doc_id):
  if 'logged_in' not in request.session or not request.session['user_level'] == "Admin":
    return redirect('/')
  if request.method == "GET":
    context = {
      'rec_info': Receive.objects.get(id=doc_id),
      'cus_sup_info': Supplier.objects.all().exclude(active=False),
      'truck_info': Truck.objects.all().exclude(active=False),
      'employees': Employee.objects.all().exclude(active=False),
      'source': 'Receiving',
      'path': 'receiving',
      'results': False,
    }
    return render(request, 'edit_rcv.html', context)
  else:
    this_record = Receive.objects.get(id=doc_id)
    errors = Receive.objects.editRSValidation(request.POST, this_record.product.lot_num)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f'/reports/receiving/{doc_id}')
    this_product = Product.objects.get(lot_num=request.POST['lot'])
    this_supplier = Supplier.objects.get(id=request.POST['supp_cust'])
    this_truck = Truck.objects.get(id=request.POST['truck'])
    this_employee = Employee.objects.get(id=request.POST['employee'])
    this_record.receive_date = request.POST['date']
    this_record.product = this_product
    this_record.qty = request.POST['qty']
    this_record.supplier = this_supplier
    this_record.trucker = this_truck
    this_record.truck_num = request.POST['truck_no']
    this_record.employee = this_employee
    this_record.save()
  return redirect('/reports/edit')

def edit_shipping(request, doc_id):
  if 'logged_in' not in request.session or not request.session['user_level'] == "Admin":
    return redirect('/')
  if request.method == "GET":
    context = {
      'rec_info': Ship.objects.get(id=doc_id),
      'cus_sup_info': Customer.objects.all().exclude(active=False),
      'truck_info': Truck.objects.all().exclude(active=False),
      'employees': Employee.objects.all().exclude(active=False),
      'source': 'Shipping',
      'path': 'shipping',
      'results': False,
    }
    return render(request, 'edit_shp.html', context)
  else:
    this_record = Ship.objects.get(id=doc_id)
    errors = Ship.objects.editRSValidation(request.POST, this_record.product.lot_num)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f'/reports/shipping/{doc_id}')
    this_product = Product.objects.get(lot_num=request.POST['lot'])
    this_customer = Customer.objects.get(id=request.POST['supp_cust'])
    this_truck = Truck.objects.get(id=request.POST['truck'])
    this_employee = Employee.objects.get(id=request.POST['employee'])
    this_record.ship_date = request.POST['date']
    this_record.product = this_product
    this_record.qty = request.POST['qty']
    this_record.customer = this_customer
    this_record.trucker = this_truck
    this_record.truck_num = request.POST['truck_no']
    this_record.employee = this_employee
    this_record.save()
  return redirect('/reports/edit')

def edit_incoming(request, doc_id):
  if 'logged_in' not in request.session or not request.session['user_level'] == "Admin":
    return redirect('/')
  if request.method == "GET":
    this_product = Product.objects.get(id=doc_id)
    context = {
      'rec_info': this_product,
      'source': 'Incoming',
      'path': 'incoming',
      'results': False,
    }
    return render(request, 'edit_inc.html', context)
  else:
    this_record = Product.objects.get(id=doc_id)
    errors = Product.objects.editFIValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f'/reports/incoming/{doc_id}')
    this_record.lot_num=request.POST['lot']
    this_record.prod_name = request.POST['product']
    this_record.best_by = request.POST['best_by']
    this_record.save()
  return redirect('/reports/edit')

def edit_finished(request, doc_id):
  if 'logged_in' not in request.session or not request.session['user_level'] == "Admin":
    return redirect('/')
  if request.method == "GET":
    this_product = Product.objects.get(id=doc_id)
    context = {
      'rec_info': this_product,
      'source': 'Finished',
      'path': 'finished',
      'results': False,
    }
    return render(request, 'edit_inc.html', context)
  else:
    this_record = Product.objects.get(id=doc_id)
    errors = Product.objects.editFIValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f'/reports/finished/{doc_id}')
    this_record.lot_num=request.POST['lot']
    this_record.prod_name = request.POST['product']
    this_record.best_by = request.POST['best_by']
    this_record.save()
  return redirect('/reports/edit')
