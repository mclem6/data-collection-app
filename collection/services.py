from django.db.models import Count, Q

from .models import Prompt, Submission

TARGET_PER_DIALECT = 5


def next_prompt(user, dialect, skipped_ids=()):
    done_ids = Submission.objects.filter(contributor=user).values_list("prompt_id", flat=True)
    return (
        Prompt.objects.filter(is_active=True)
        .exclude(id__in=done_ids)
        .exclude(id__in=skipped_ids)
        .annotate(
            n=Count(
                "submissions",
                filter=Q(submissions__dialect=dialect) & ~Q(submissions__status=Submission.Status.REJECTED),
            )
        )
        .filter(n__lt=TARGET_PER_DIALECT)
        .order_by("?")
        .first()
    )