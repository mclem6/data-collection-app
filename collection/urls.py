from django.urls import path

from . import views

urlpatterns = [
    path("", views.record, name="home"),
    path("skip/", views.skip, name="skip"),
]