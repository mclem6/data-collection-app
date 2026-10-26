from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User


@admin.register(User)
class  CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "name", "dialect", "is_blocked")
    search_fields = ("email", "name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": ("name", "dialect", "is_blocked")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

