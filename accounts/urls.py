from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.request_code, name="login"),
    path("verify/", views.verify_code, name="verify"),
    path("onboarding/", views.onboarding, name="onboarding"),
]