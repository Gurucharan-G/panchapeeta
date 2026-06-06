from django.urls import path
from . import views

app_name = 'peethas'

urlpatterns = [
    path('', views.home, name='home'),
    path('peetha/<slug:slug>/', views.peetha_detail, name='peetha_detail'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/peetha/<slug:slug>/', views.dashboard_peetha, name='dashboard_peetha'),
    
    # Media CRUD
    path('dashboard/peetha/<slug:slug>/media/add/', views.media_add, name='media_add'),
    path('dashboard/peetha/<slug:slug>/media/<int:pk>/edit/', views.media_edit, name='media_edit'),
    path('dashboard/peetha/<slug:slug>/media/<int:pk>/delete/', views.media_delete, name='media_delete'),
    
    # Travel CRUD
    path('dashboard/peetha/<slug:slug>/travel/add/', views.travel_add, name='travel_add'),
    path('dashboard/peetha/<slug:slug>/travel/<int:pk>/edit/', views.travel_edit, name='travel_edit'),
    path('dashboard/peetha/<slug:slug>/travel/<int:pk>/delete/', views.travel_delete, name='travel_delete'),
]

