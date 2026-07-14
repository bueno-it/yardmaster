from django.urls import path
from . import views
urlpatterns = [
    path('',                  views.plan_list,      name='plan_list'),
    path('api/update-cell/',    views.update_cell,    name='dp_update_cell'),
    path('api/update-flag/',    views.update_flag,    name='dp_update_flag'),
    path('api/import-plan/',  views.import_plan,    name='dp_import_plan'),
    path('api/import-picking/', views.import_picking, name='dp_import_picking'),
    path('api/add-row/',      views.add_row,        name='dp_add_row'),
    path('api/delete-row/',   views.delete_row,     name='dp_delete_row'),
    path('export/',           views.export_plan,    name='dp_export'),
]
