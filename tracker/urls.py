from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('signup/', views.signup_view, name='signup'),
     path('transactions/', views.transaction_list, name='transaction_list'),
     path('add-budget/', views.add_budget, name='add_budget'),
     path('export/csv/', views.export_transactions_csv, name='export_csv'),

     
]
