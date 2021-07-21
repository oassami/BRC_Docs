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
    if this_product.type == 'I':


      prod_products = ProdProduct.objects.select_related('product', 'production').filter(product=this_product)
      if prod_products:
        for x in prod_products:
          print(x.product.lot_num)
          print(x.product.prod_name)
          print(x.production.production_date)

      context = {
        
        'results': True,
        'product_type': 'I'
      }


    else:
      prod_product = ProdProduct.objects.select_related('production', 'product').get(product=this_product)
      # print('Lot #: ', prod_product.product.lot_num)
      # print('Product Name: ', prod_product.product.prod_name)
      # print('Best By Date: ', prod_product.product.best_by)
      # print('QTY: ', prod_product.quantity)
      # print('Productioin Date: ', prod_product.production.production_date)
      ship_to_customers = Ship.objects.select_related('customer', 'trucker', 'employee').filter(product=this_product)
      qty_shipped = 0
      qty_on_hand = 0 
      if ship_to_customers:
        for ship_to in ship_to_customers:
          qty_shipped += ship_to.qty
          qty_on_hand = prod_product.quantity - qty_shipped
          # print('Customer Name: ', ship_to.customer.name)
          # print('QTY to this Customer: ', ship_to.qty)
          # print('Shipping Date: ', ship_to.ship_date)
          # print('Trucking Company: ', ship_to.trucker.name)
          # print('Truck #: ', ship_to.truck_num)
          # print('Shipped By: ', ship_to.employee.first_name)
        recovered = int(100-(((prod_product.quantity - (qty_shipped + qty_on_hand))/prod_product.quantity)*100))
        # print('recovered', recovered)
      context = {
        'prod_product': prod_product,
        'ship_to_customers': ship_to_customers,
        'qty_shipped': qty_shipped,
        'qty_on_hand': prod_product.quantity - qty_shipped,
        'recovered': recovered,
        'results': True,
        'product_type': 'F'
      }
  return render(request, 'forward.html', context)

def backward(request):
  if 'logged_in' not in request.session:
    return redirect('/')
  return render(request, 'backward.html')

