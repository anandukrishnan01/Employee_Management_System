from django.urls import path

from .views import EmployeeListCreateAPI, EmployeeDetailAPI

app_name = "employees"

urlpatterns = [
    path("employees/", EmployeeListCreateAPI.as_view()),
    path("employees/<uuid:pk>/", EmployeeDetailAPI.as_view()),
]
