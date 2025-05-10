from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import HttpResponsePermanentRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .hfunctions import *
from .models import MoexIndexData

def HomePage(request):
    logedusername = "Unknown user"
    if request.user.is_authenticated:
        logedusername = request.user.username
    return render(request, 'home.html', {'username': logedusername})

def LogOutRequest(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def LoginRequest(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        return render(request, 'login.html')

def MoexPage(request):
    data = MoexIndexData.objects.all().order_by('-weight')
    return render(request, 'moexpage.html', {'data': data})

def PortfoliosPage(request):
    return render(request, 'folios.html')

@login_required
@csrf_protect
def LoadMoexRequest(request):
    if request.method == 'POST':
        moexdatajson = getimoexindex()
        if moexdatajson:
            save_moex_data_from_json(moexdatajson)
            messages.success(request, 'Данные успешно загружены!')
        else:
            messages.error(request, 'Ошибка при загрузке данных.')
        return redirect('moex')
    return redirect('moex')

