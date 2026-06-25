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
    path('profile/', views.profile_view, name='profile_view'),
    
    # Dashboard
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/peetha/<slug:slug>/', views.dashboard_peetha, name='dashboard_peetha'),
    path('dashboard/peetha/<slug:slug>/update-live/', views.update_peetha_live, name='update_peetha_live'),
    path('dashboard/assign-handler/', views.assign_handler, name='assign_handler'),
    path('dashboard/create-user-account/', views.create_user_account, name='create_user_account'),
    path('dashboard/payment-config/', views.manage_payment_config, name='manage_payment_config'),
    path('dashboard/payment-config/<int:pk>/delete/', views.delete_payment_config, name='delete_payment_config'),
    path('dashboard/toggle-feature/<int:pk>/', views.toggle_feature, name='toggle_feature'),
    
    # Media CRUD
    path('dashboard/peetha/<slug:slug>/media/add/', views.media_add, name='media_add'),
    path('dashboard/peetha/<slug:slug>/media/<int:pk>/edit/', views.media_edit, name='media_edit'),
    path('dashboard/peetha/<slug:slug>/media/<int:pk>/delete/', views.media_delete, name='media_delete'),
    
    # Travel CRUD
    path('dashboard/peetha/<slug:slug>/travel/add/', views.travel_add, name='travel_add'),
    path('dashboard/peetha/<slug:slug>/travel/<int:pk>/edit/', views.travel_edit, name='travel_edit'),
    path('dashboard/peetha/<slug:slug>/travel/<int:pk>/delete/', views.travel_delete, name='travel_delete'),
    
    # Pooja CRUD
    path('dashboard/peetha/<slug:slug>/pooja/add/', views.pooja_add, name='pooja_add'),
    path('dashboard/peetha/<slug:slug>/pooja/<int:pk>/edit/', views.pooja_edit, name='pooja_edit'),
    path('dashboard/peetha/<slug:slug>/pooja/<int:pk>/delete/', views.pooja_delete, name='pooja_delete'),
    
    # Pooja Booking
    path('peetha/<slug:peetha_slug>/book-pooja/', views.initiate_pooja_booking, name='initiate_pooja_booking'),
    path('peetha/<slug:peetha_slug>/pooja/<int:pooja_id>/availability/', views.pooja_availability, name='pooja_availability'),
    path('verify-pooja-payment/', views.verify_pooja_payment, name='verify_pooja_payment'),
    
    # Dashboard AJAX APIs
    path('dashboard/api/date-bookings/', views.dashboard_date_bookings, name='dashboard_date_bookings'),
    path('dashboard/api/search-devotees/', views.dashboard_search_devotees, name='dashboard_search_devotees'),
]

