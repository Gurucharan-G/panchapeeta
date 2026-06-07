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
    list_display = ('name', 'peetha', 'price', 'is_active', 'order')
    list_filter = ('peetha', 'is_active')
    ordering = ('peetha', 'order')

@admin.register(PoojaBooking)
class PoojaBookingAdmin(admin.ModelAdmin):
    list_display = ('devotee_name', 'pooja', 'date_of_pooja', 'amount', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'pooja__peetha', 'date_of_pooja')
    search_fields = ('devotee_name', 'devotee_phone', 'devotee_email', 'razorpay_order_id')
    readonly_fields = ('created_at',)
