from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User
import bcrypt

def index(request):
  if 'logged_in' in request.session:
    request.session.clear()
  if not User.objects.filter(level="Admin"):
    request.session['register'] = True
  return render(request, 'login.html')

def user_login(request):
  request.session.clear()
  request.session['email'] = request.POST['email']
  errors = User.objects.loginValidation(request.POST)
  if errors:
      for key, value in errors.items():
          messages.error(request, value)
      return redirect('/')
  try:
      user = User.objects.get(email = request.POST['email'])
      if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
          messages.error(request, 'Incorrect email address or password.')
          return redirect('/')
  except:
      messages.error(request, 'Incorrect email address or password.')
      return redirect('/')
  request.session['user_id'] = user.id
  request.session['first_name'] = user.first_name
  request.session['last_name'] = user.last_name
  request.session['user_level'] = user.level
  request.session['logged_in'] = "logged_in"
  return redirect('/brc')

def user_register(request):
  if request.method == "GET":
    if 'logged_in' in request.session:
      request.session.clear()
    return render(request, 'register.html')
  else:
    request.session.clear()
    request.session['first_name']= request.POST['first_name']
    request.session['last_name']= request.POST['last_name']
    request.session['email']= request.POST['email']
    errors = User.objects.addValidation(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/user/register')
    if not User.objects.filter(level="Admin"):
      user_level = "Admin" # admin
    else:
      user_level = "Normal" # regular user
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
        level = user_level
    )
    request.session['user_id'] = user.id
    request.session['user_level'] = user.level
    request.session['logged_in'] = "logged_in"
  return redirect('/brc')

# def clear_forms(request):
#   request.session.clear()
#   return redirect('/')

# def pw_reset(request):
#   if request.method == "POST":
#       request.session.clear()
#       errors = User.objects.resetValidation(request.POST)
#       if errors:
#           for key, value in errors.items():
#               messages.error(request, value)
#           return redirect('/user/pw_reset')
#       request.session['email'] = request.POST['email']
#       request.session['password'] = request.POST['password']
#       return redirect('/reseted')
#   return render(request, 'reset.html')

# def reseted(request):
#   try:
#       user = User.objects.get(email = request.session['email'])
#   except:
#       messages.error(request, 'email address not found.')
#       return redirect('/user/pw_reset')
#   pw_hash = bcrypt.hashpw(request.session['password'].encode(), bcrypt.gensalt()).decode()
#   user.password = pw_hash
#   user.save()
#   messages.info(request, "Reset successful...! Please log in...")
#   return redirect('/')
