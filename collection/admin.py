from django.contrib import admin
from .models import Prompt, Submission

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("text", "is_active", "created_at")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("contributor", "prompt", "dialect", "status", "created_at")
    list_filter = ("status", "dialect")
    search_fields = ("contributor__email", "transcription")
