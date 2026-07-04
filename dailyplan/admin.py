from django.contrib import admin
from .models import DailyPlan

@admin.register(DailyPlan)
class DailyPlanAdmin(admin.ModelAdmin):
    list_display  = ['date', 'store_display', 'store_id_raw', 'ordered', 'remaining', 'picked', 'is_complete']
    list_filter   = ['date', 'hb_bd']
    search_fields = ['store__name', 'store_name_raw', 'store_id_raw']
    date_hierarchy = 'date'
