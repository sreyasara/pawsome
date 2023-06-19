import logging
from pprint import pprint

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from home.models import Cart
from .models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signin(request):
    context1 = {}
    pprint(request.META['QUERY_STRING'])
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, password)
        if not email or not password:
            context1['pswderr'] = "Email and password cannot be empty"
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            redirect_location = request.GET.get('next', '/') + '?' + request.META['QUERY_STRING']
            return HttpResponseRedirect(redirect_location)
        else:
            # Return an 'invalid login' error message.
            context1['pswderr'] = "Invalid Credentials"
    return render(request, template_name="account/login.html", context=context1)


@csrf_exempt
def signup(request):
    context1 = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password1")
        passwrd2 = request.POST.get("password2")
        username = request.POST.get("username", '')
        name = request.POST.get("name", '')
        first_name = name.split(' ')[0]
        if len(name.split(' ')) > 1:
            last_name = name.split(' ')[1]
        else:
            last_name = ''

        if not email:
            context1['pswderr'] = 'Email cannot be empty'
        elif not password or not passwrd2:
            context1['pswderr'] = 'Password cannot be empty'
        elif not username:
            context1['pswderr'] = 'Username cannot be empty'
        else:
            if passwrd2 == password:
                try:
                    user = User.objects.create_user(email=email, password=password, username=username,
                                                    first_name=first_name, last_name=last_name)

                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    Cart.objects.create(user=user)
                    redirect_location = request.GET.get('next', '/') + '?' + request.META['QUERY_STRING']
                    return HttpResponseRedirect(redirect_location)

                except User.DoesNotExist as e:
                    print(e)

                    context1['pswderr'] = 'User already exists'
                except Exception as e:
                    print(e)
                    context1['pswderr'] = 'Something went wrong'

            else:

                context1['pswderr'] = 'Password Does not match'

    return render(request, template_name="account/signup.html", context=context1)


@login_required
def log_out(request):
    if request.method == "POST":
        logout(request)
        url = '/?' + request.META['QUERY_STRING']
        return HttpResponseRedirect(url)

    return render(request, template_name="account/logout.html")
