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
    'all_employees': Employee.objects.all().order_by('emp_id'),
  }
  return render(request, 'employees_list.html', context)

def employee_add(request):
  if 'logged_in' not in request.session:
      return redirect('/')
  if request.method == "GET":
    return render(request, 'employee_add_edit.html')
  else:
    errors = Employee.objects.addValidation(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/brc/employee/add')
    employee = Employee.objects.create(
        emp_id = request.POST['emp_id'],
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        level = request.POST['level'],
    )
  return redirect('/brc/employees')

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
    errors = Employee.objects.editValidation(request.POST, emp)
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
  return redirect('/brc/employees')

def employee_delete(request, emp_id):
  if 'logged_in' in request.session:
    try:
      emp = Employee.objects.get(id=emp_id)
      emp.delete()
    except:
      pass
  else:
    return redirect('/')
  return redirect('/brc/employees')

def customers(request):
  pass
  return render(request, 'users_list.html', context)

def customer_add(request):
  pass
  return redirect('/brc')

def customer_edit(request, user_id):
  pass
  return redirect('/brc')

def customer_delete(request, user_id):
  pass
  return redirect('/brc')

def suppliers(request):
  pass
  return render(request, 'users_list.html', context)

def supplier_add(request):
  pass
  return redirect('/brc')

def supplier_edit(request, user_id):
  pass
  return redirect('/brc')

def supplier_delete(request, user_id):
  pass
  return redirect('/brc')

def trucking(request):
  pass
  return render(request, 'users_list.html', context)

def trucking_add(request):
  pass
  return redirect('/brc')

def trucking_edit(request, user_id):
  pass
  return redirect('/brc')

def trucking_delete(request, user_id):
  pass
  return redirect('/brc')

# def display_snack(request, snack_id):
#   logged_user = User.objects.get(id=request.session['user_id'])
#   this_snack = Snack.objects.get(id=snack_id)
#   users_like = this_snack.likes.all()
#   users_dislike = this_snack.dislikes.all()
#   logged_user_like = False
#   logged_user_dislike = False
#   if logged_user in users_like:
#     logged_user_like = True
#   if logged_user in users_dislike:
#     logged_user_dislike = True
#   context = {
#     'this_snack': this_snack,
#     'users_like': users_like,
#     'users_dislike': users_dislike,
#     'logged_user_like': logged_user_like,
#     'logged_user_dislike': logged_user_dislike,
#   }
#   return render(request, 'snack_disp.html', context)


# def user_edit(request):
#   user = User.objects.get(id=request.session['user_id'])
#   if request.method == 'GET':
#     context={
#       'this_user': user,
#     }
#     return render(request, 'user_edit.html', context)
#   else:
#     errors = User.objects.editValidator(request.POST, user)
#     if errors:
#       for key, value in errors.items():
#         messages.error(request, value)
#       return redirect('/snacks/user/edit')
#     if request.POST['first_name']:
#       user.first_name = request.POST['first_name']
#     if request.POST['last_name']:
#       user.last_name = request.POST['last_name']
#     if request.POST['email']:
#       user.email = request.POST['email']
#       request.session['email'] = user.email
#     if request.POST['password']:
#       user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
#     user.save()
#   return redirect(f'/snacks/user/{user.id}')




# def like_snack(request, snack_id):
#   this_user = User.objects.get(id=request.session['user_id'])
#   this_snack = Snack.objects.get(id=snack_id)
#   this_snack.likes.add(this_user)
#   this_snack.dislikes.remove(this_user)
#   return redirect(f'/snacks/{snack_id}')

# def dislike_snack(request, snack_id):
#   this_user = User.objects.get(id=request.session['user_id'])
#   this_snack = Snack.objects.get(id=snack_id)
#   this_snack.likes.remove(this_user)
#   this_snack.dislikes.add(this_user)
#   return redirect(f'/snacks/{snack_id}')
