import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import *
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.gis.geos import Point


def user_register(request):
    if request.user.is_authenticated:
        return redirect('world')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'User Registration Successful!')
                return redirect('world')
            else:
                messages.error(request, 'Error: Something Went Wrong.')
        else:
            form = UserRegisterForm()

        return render(request, 'world/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('world')
    else:
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('world')
        else:
            form = UserLoginForm()
        return render(request, 'world/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def world(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        context = {'title': 'Leaflet Map'}
        return render(request, 'world/world.html', context)


def update_location(request):
    data = json.loads(request.body)
    lat = data['latitude']
    lng = data['longitude']

    request.user.last_location = Point(lng, lat)

    request.user.save()
    request.user.refresh_from_db()

    return JsonResponse('Item Added', safe=False)
