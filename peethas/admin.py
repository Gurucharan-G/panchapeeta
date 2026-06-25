from django.contrib import admin
from .models import Peetha


@admin.register(Peetha)
class PeethaAdmin(admin.ModelAdmin):
    list_display = ('name', 'acharya', 'location', 'color', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


from .models import PeethaPaymentConfig, Pooja, PoojaBooking

@admin.register(PeethaPaymentConfig)
class PeethaPaymentConfigAdmin(admin.ModelAdmin):
    list_display = ('peetha', 'is_active')

@admin.register(Pooja)
class PoojaAdmin(admin.ModelAdmin):
    list_display = ('name', 'peetha', 'category', 'price', 'total_slots', 'available_days', 'is_active', 'order')
    list_filter = ('peetha', 'is_active', 'category')
    ordering = ('peetha', 'order')

@admin.register(PoojaBooking)
class PoojaBookingAdmin(admin.ModelAdmin):
    list_display = ('devotee_name', 'pooja', 'date_of_pooja', 'amount', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'pooja__peetha', 'date_of_pooja')
    search_fields = ('devotee_name', 'devotee_phone', 'devotee_email', 'razorpay_order_id', 'gotra')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Booking Info', {
            'fields': ('pooja', 'user', 'devotee_name', 'devotee_phone', 'devotee_email', 'date_of_pooja')
        }),
        ('Sankalpa Details', {
            'fields': ('gotra', 'nakshatra', 'rashi', 'family_members'),
            'classes': ('collapse',),
        }),
        ('Payment', {
            'fields': ('amount', 'payment_status', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at'),
        }),
    )
