from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', HomePage, name='home'),
    path('moex/', MoexPage, name='moex'),
    path('securities/', SecuritiesPage, name='securities'),
    path('folios/', PortfoliosPage, name='folios'),
    path('folios/<int:folio_id>/', FolioDetails, name='view_folio'),
    path('newfolio/', NewFolioPage, name='new_folio'),
    path('login/', LoginRequest, name='login'),
    path('logout/', LogOutRequest, name='logout'),
    path('loadmoex/', LoadMoexRequest, name='load_moex'),
    path('loadsecurities/', LoadSecuritiesRequest, name='load_securities'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)