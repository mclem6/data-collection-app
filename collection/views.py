from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def home(request):
    return HttpResponse(f"Signed in as {request.user.email}. Recording page coming next.")