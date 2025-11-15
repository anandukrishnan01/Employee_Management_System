from django.urls import path

from accounts.views import register_view, logout_view, change_password, profile_view, profile_update_view

app_name = "accounts"

urlpatterns = [

    path("register/",  register_view, name="register"),
    path("logout/",  logout_view, name="logout"),
    path("change-password/",  change_password, name="change_password"),
    path("profile/",  profile_view, name="profile"),
    path("profile/update/", profile_update_view, name="profile_update"),

]
