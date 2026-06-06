from django.urls import path
from . import views

app_name = 'peethas'

urlpatterns = [
    path('', views.home, name='home'),
    path('peetha/<slug:slug>/', views.peetha_detail, name='peetha_detail'),
]
