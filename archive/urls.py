from django.urls import path
from . import views

urlpatterns = [
    path('', views.archive_page, name ='archive_page'),
]