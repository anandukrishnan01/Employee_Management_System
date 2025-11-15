from django.urls import path

from .views import builder_view, template_list, edit_template, delete_template, save_template

app_name = "forms"

urlpatterns = [
    path("builder/",  builder_view, name="builder"),
    path("builder/save/", save_template, name="save_template"),
    path("templates/",  template_list, name="template_list"),
    path("templates/<slug:slug>/edit/",  edit_template, name="edit_template"),
    path("templates/<slug:slug>/delete/",  delete_template, name="delete_template"),
]
