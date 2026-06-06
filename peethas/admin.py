from django.contrib import admin
from .models import Peetha


@admin.register(Peetha)
class PeethaAdmin(admin.ModelAdmin):
    list_display = ('name', 'acharya', 'location', 'color', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)
