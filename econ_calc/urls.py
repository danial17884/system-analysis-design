from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.econ_calculator, name='econ_calculator'), 
]
