from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.request_code, name="login"),
    path("verify/", views.verify_code, name="verify"),
    path("onboarding/", views.onboarding, name="onboarding"),
    path("logout/", LogoutView.as_view(), name="logout"),
]