from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import SubmissionForm
from .models import Prompt, Submission
from .services import next_prompt


@login_required
def record(request):
    user = request.user
    if not user.name:
        return redirect("accounts:onboarding")

    prompt = None
    prompt_id = request.session.get("current_prompt")
    if prompt_id:
        prompt = (
            Prompt.objects.filter(id=prompt_id, is_active=True)
            .exclude(submissions__contributor=user)
            .first()
        )
    if prompt is None:
        prompt = next_prompt(user, user.dialect, request.session.get("skipped", []))
        request.session["current_prompt"] = prompt.id if prompt else None

    form = SubmissionForm(request.POST or None, request.FILES or None, initial={"dialect": user.dialect})
    if prompt and request.method == "POST" and form.is_valid():
        submission = form.save(commit=False)
        submission.contributor = user
        submission.prompt = prompt
        submission.save()
        request.session.pop("current_prompt", None)
        return redirect("home")

    count = Submission.objects.filter(contributor=user).count()
    return render(request, "collection/record.html", {"prompt": prompt, "form": form, "count": count})


@login_required
@require_POST
def skip(request):
    current = request.session.pop("current_prompt", None)
    if current:
        skipped = request.session.get("skipped", [])
        skipped.append(current)
        request.session["skipped"] = skipped
    return redirect("home")