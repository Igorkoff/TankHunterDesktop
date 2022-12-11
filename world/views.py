import json

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.gis.geos import Point
from django.http import JsonResponse


from .forms import UserRegisterForm, UserLoginForm, UserReportForm
from .models import *


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

        context = {'title': 'Register', 'form': form}
        return render(request, 'world/register.html', context)


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

        context = {'title': 'Login', 'form': form}
        return render(request, 'world/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


def world(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.user.is_staff or request.user.is_admin:
            convoys = Convoy.objects.filter(tracking=True)
            reports = Report.objects.filter(verified=True)
            context = {'title': 'Map', 'convoys': convoys, 'reports': reports}
        else:
            context = {'title': 'Map'}

        return render(request, 'world/world.html', context)


def update_location(request):
    data = json.loads(request.body)
    lat = data['latitude']
    lng = data['longitude']

    request.user.last_location = Point(lng, lat)

    request.user.save()
    request.user.refresh_from_db()

    return JsonResponse('Item Added', safe=False)


def create_report(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = UserReportForm(request.POST, request.FILES)
            if form.is_valid():
                report = form.save(commit=False)

                report.user = request.user
                report.location = request.user.last_location

                report.save()
                report.refresh_from_db()

                messages.success(request, 'Thank You for Your Service.')
                return redirect('world')
            else:
                messages.error(request, 'Error: Something Went Wrong.')
        else:
            form = UserReportForm()

        context = {'title': 'Report the Enemy', 'form': form}
        return render(request, 'world/report.html', context)


def error_404_view(request, exception):
    context = {'title': 'Error 404', 'error_message': 'Page Not Found'}
    return render(request, 'world/error.html', context)


def error_500_view(request):
    context = {'title': 'Error 500', 'error_message': 'Internal Server Error'}
    return render(request, 'world/error.html', context)