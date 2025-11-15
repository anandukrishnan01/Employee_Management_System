from django.urls import path
from . import views
from .views import employee_list, employee_create, employee_update, employee_save, employee_delete, employee_save_update

app_name = "employees"

urlpatterns = [
    path("list/",  employee_list, name="employee_list"),
    path("create/<slug:slug>/",  employee_create, name="employee_create"),
    path("edit/<uuid:pk>/",  employee_update, name="employee_update"),

    # AJAX
    path("ajax/save/<slug:slug>/",  employee_save, name="employee_save"),
    path("ajax/save_update/<uuid:pk>/",  employee_save_update, name="employee_save_update"),
    path("ajax/delete/<uuid:pk>/",  employee_delete, name="employee_delete"),
]

