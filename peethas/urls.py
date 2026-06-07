from django.urls import path
from . import views

app_name = 'peethas'

urlpatterns = [
    path('', views.home, name='home'),
    path('peetha/<slug:slug>/', views.peetha_detail, name='peetha_detail'),
    
    # Auth & Devotee
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('verify-firebase-token/', views.verify_firebase_token, name='verify_firebase_token'),
    
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
    
    # Pooja Booking
    path('peetha/<slug:peetha_slug>/book-pooja/', views.initiate_pooja_booking, name='initiate_pooja_booking'),
    path('verify-pooja-payment/', views.verify_pooja_payment, name='verify_pooja_payment'),
]

