from django.urls import path

from .views import FormTemplateListCreateAPI, FormTemplateDetailAPI

app_name = "forms"

urlpatterns = [
    path("templates/", FormTemplateListCreateAPI.as_view()),
    path("templates/<slug:slug>/", FormTemplateDetailAPI.as_view()),
]
