from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
      path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('signup/', views.signup_view, name='signup'),
     path('transactions/', views.transaction_list, name='transaction_list'),
  #   path('add-budget/', views.add_budget, name='add_budget'),
     path('export/csv/', views.export_transactions_csv, name='export_csv'),
     path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('transactions/', views.transaction_list, name='transactions'),

    path('statistics/', views.statistics_view, name='statistics'),
    path('profile/', views.profile_view, name='profile'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('api/chart-data/', views.chart_data_api, name='chart_data_api'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('about/', views.about_view, name='about'),
    path('404/', views.error_404_view, name='404'),
     
]
