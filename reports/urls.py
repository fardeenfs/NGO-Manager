from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.reportshome, name="reports home"),
    path('get-carried-balances/', views.getkudishika, name="carried balances report"),
    path('incomevoucher/',views.incomevoucher,name="income voucher reports"),
    path('expensevoucher/',views.expensevoucher,name="expense voucher reports"),
    path('duepaidreports/',views.due_paid_reports,name="due paid reports"),
    path('duenotpaidreports/',views.due_not_paid_reports,name="due not paid reports"),
    path('cancelledduesreports/',views.cancelled_due_reports,name="cancelled due reports"),
    path('inactivemembersreports/',views.inactive_members_reports,name="inactive members reports"),
    ]