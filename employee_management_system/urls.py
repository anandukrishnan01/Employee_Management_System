
from django.contrib import admin
from django.urls import path, include

from accounts.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("forms/", include("forms.urls")),
    path("employees/", include("employees.urls")),

    path("",  login_view, name="login"),
    # rest_framework urls
    path('api/v1/accounts/', include('api.v1.accounts.urls', namespace="api_v1_accounts")),
    path('api/v1/forms/', include('api.v1.forms.urls', namespace="api_v1_forms")),
    path('api/v1/employee/', include('api.v1.employees.urls', namespace="api_v1_employees")),


]
