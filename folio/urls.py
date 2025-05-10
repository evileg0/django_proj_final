from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', HomePage, name='home'),
    path('moex/', MoexPage, name='moex'),
    path('folios/', PortfoliosPage, name='folios'),
    path('login/', LoginRequest, name='login'),
    path('logout/', LogOutRequest, name='logout'),
    path('loadmoex/', LoadMoexRequest, name='load_moex'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)