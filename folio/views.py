from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import HttpResponsePermanentRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .hfunctions import *
from .models import MoexIndexData, Folio, SecuritiesIndexData, FolioSecurity
from .forms import FolioForm

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
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        return render(request, 'login.html')

def MoexPage(request):
    moex_data = MoexIndexData.objects.all().order_by('-weight')
    return render(request, 'moexpage.html', {'data': moex_data})

def SecuritiesPage(request):
    securities_data = SecuritiesIndexData.objects.all().order_by('shortname')
    return render(request, 'securities.html', {'data': securities_data})

@login_required
def PortfoliosPage(request):
    folios = Folio.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'folios.html', {'folios': folios})

@login_required
def NewFolioPage(request):
    if request.method == 'POST':
        form = FolioForm(request.POST)
        if form.is_valid():
            folio = form.save(commit=False)
            folio.user = request.user
            folio.save()
            messages.success(request, 'Портфель успешно создан!')
            return redirect('folios')
    else:
        form = FolioForm()

    return render(request, 'newfolio.html', {'form': form})

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

@login_required
@csrf_protect
def LoadSecuritiesRequest(request):
    if request.method == 'POST':
        securitiesdatajson = getsecuritiesindex()
        if securitiesdatajson:
            save_securities_data_from_json(securitiesdatajson)
            messages.success(request, 'Данные успешно загружены!')
        else:
            messages.error(request, 'Ошибка при загрузке данных.')
        return redirect('securities')
    return redirect('securities')

@login_required
def FolioDetails(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id, user=request.user)
    securities_in_folio = folio.securities.all().order_by('security__shortname')

    if request.method == 'POST':
        secid = request.POST.get('secid')
        quantity = int(request.POST.get('quantity', 1))

        try:
            security = SecuritiesIndexData.objects.get(secid=secid)
            folio_security, created = FolioSecurity.objects.get_or_create(
                folio=folio,
                security=security,
                defaults={'quantity': quantity}
            )
            if not created:
                # Если уже существует — увеличиваем количество
                folio_security.quantity += quantity
                folio_security.save(update_fields=['quantity'])
            messages.success(request, f"Добавлено: {security.shortname}")
        except SecuritiesIndexData.DoesNotExist:
            messages.error(request, "Выбранная ценная бумага не найдена")
        except Exception as e:
            messages.error(request, f"Ошибка: {e}")

        return redirect('view_folio', folio_id=folio.id)

    available_securities = SecuritiesIndexData.objects.all().order_by('shortname')

    total_value = 0
    for item in securities_in_folio:
        if item.security and item.quantity:
            try:
                total_value += float(item.security.prevprice) * float(item.quantity)
            except (ValueError, TypeError):
                pass

    context = {
        'folio': folio,
        'available_securities': available_securities,
        'securities_in_folio': securities_in_folio,
        'total_value': round(total_value, 2),
    }
    return render(request, 'folio_details.html', context)