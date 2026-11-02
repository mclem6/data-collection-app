
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("collection.urls")),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
