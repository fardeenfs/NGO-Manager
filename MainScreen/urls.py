from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homeloaded, name="home"),
    path('dues/',views.getdues, name="dues"),
    path('apply-dues/',views.applydues, name="dues"),
    path('apply-due-manual/',views.manual_due_apply, name="manual due"),
    path('new-due/',views.newdue,name="new due"),
    path('account-reports/',views.accountview,name="account-reports"),
    path('invoice/',views.printinvoice,name="invoice-print"),
    path('new-member/',views.newmember,name="new member"),
    path('new-family/',views.newfamily,name="new family"),
    path('edit-member/',views.editmember,name="member edit"),
    path('dues-settings/',views.dueslist,name="all dues"),
    path('edit-dues/',views.edit_dues,name="edit dues"),
    path('due-override/',views.override_due,name="due override"),
    path('mark-paid/',views.mark_as_paid,name="mark as paid"),
    path('undo-mark-as-paid/',views.undo_mark_as_paid,name="undo mark as paid"),
    path('cancel-receipt/',views.cancel_receipt,name="cancel receipt"),
    path('temporary-accounts-add-20202021',views.temporaryadd,name="Temporary Code")
]
