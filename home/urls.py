from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_page, name ='home_page'),
    path('', views.home_page, name ='home_page'),
]