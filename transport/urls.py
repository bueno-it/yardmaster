from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_list, name='load_list'),

    # Load APIs
    path('api/update-cell/',  views.update_cell,  name='update_cell'),
    path('api/update-flag/',  views.update_flag,  name='update_flag'),
    path('api/add-load/',     views.add_load,     name='add_load'),
    path('api/delete-load/',  views.delete_load,  name='delete_load'),
    path('api/import/',       views.import_csv,   name='import_csv'),
    path('api/options/',      views.api_options,  name='api_options'),
    path('export/',           views.export_csv,   name='export_csv'),

    # Stores
    path('stores/',           views.store_list,   name='store_list'),
    path('api/store/save/',   views.store_save,   name='store_save'),
    path('api/store/delete/', views.store_delete, name='store_delete'),

    # Drivers
    path('drivers/',           views.driver_list,   name='driver_list'),
    path('api/driver/save/',   views.driver_save,   name='driver_save'),
    path('api/driver/delete/', views.driver_delete, name='driver_delete'),

    # Companies
    path('companies/',           views.company_list,   name='company_list'),
    path('api/company/save/',    views.company_save,   name='company_save'),
    path('api/company/delete/',  views.company_delete, name='company_delete'),
]
