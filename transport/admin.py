from django.contrib import admin
from .models import Load, Store, Driver, Company

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'store_code', 'active']
    search_fields = ['name', 'store_code']
    list_filter = ['active']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    search_fields = ['name']
    list_filter = ['active']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    search_fields = ['name']
    list_filter = ['active']

@admin.register(Load)
class LoadAdmin(admin.ModelAdmin):
    list_display  = ['date', 'day', 'store', 'driver', 'company', 'status']
    list_filter   = ['day', 'status', 'date']
    search_fields = ['store__name', 'driver__name', 'company__name', 'trailer_no']
    autocomplete_fields = ['store', 'driver', 'company']
    date_hierarchy = 'date'
