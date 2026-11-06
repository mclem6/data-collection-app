from django.contrib import admin
from .models import Prompt, Submission
from django.utils import timezone
from django.utils.html import format_html

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("text", "is_active", "created_at")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("prompt_text", "player", "transcription", "dialect", "status", "reviewed_by", "contributor")
    list_per_page = 25
    list_filter = ("status", "dialect", "reviewed_by")
    search_fields = ("contributor__email", "transcription")
    actions = ["approve", "reject"]

    class Media:
        js = ("collection/admin_audio.js",)

    readonly_fields = ("status", "reviewed_by", "reviewed_at")

    def has_change_permission(self, request, obj=None):
        if obj and obj.status != Submission.Status.PENDING and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status == Submission.Status.APPROVED and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    @admin.display(description="Prompt")
    def prompt_text(self, obj):
        return obj.prompt.text

    @admin.display(description="Audio")
    def player(self, obj):
        if not obj.audio:
            return "-"
        return format_html(
            '<button type="button" class="play-btn" data-src="{}" aria-label="Play">▶</button>',
            obj.audio.url,
        )
    def _review(self, request, queryset, status, label):
        pending = queryset.filter(status=Submission.Status.PENDING)
        updated = pending.update(status=status, reviewed_by=request.user, reviewed_at=timezone.now())
        skipped = queryset.count() - updated
        msg = f"{label} {updated} submission(s)."
        if skipped:
            msg += f" Skipped {skipped} that were already reviewed."
        self.message_user(request, msg)

    @admin.action(description="Approve selected", permissions=["change"])
    def approve(self, request, queryset):
        self._review(request, queryset, Submission.Status.APPROVED, "Approved")

    @admin.action(description="Reject selected", permissions=["change"])
    def reject(self, request, queryset):
        self._review(request, queryset, Submission.Status.REJECTED, "Rejected")
