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
          'prod_iproduct': prod_iproduct,
          'prod_fproduct': prod_fproduct,
          'recieved_from': recieved_from,
          'iprod': 1,
          'results': True,
          'product_type': 'F'
        }
      else:
        # print('4', prod_iproduct)
        x=1
        context={}
        for p in prod_products:
          if p.product.type == 'I':
            context[f'prod_iproduct{x}'] = p
            context[f'recieved_from{x}'] = Receive.objects.select_related('supplier', 'trucker', 'employee').get(product=p.product)
            x += 1
        context['this_product'] = this_product
        context['iprod'] = 2
        context['results'] = True
        context['product_type'] = 'F'
  return render(request, 'backward.html', context)

