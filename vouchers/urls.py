from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.voucher_view, name="home"),
    path('print/',views.printvoucher,name="print"),
    path('cancelvoucher/',views.cancelvoucher,name="cancel voucher")
]