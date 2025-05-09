from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    """Render landing view."""
    return render(request, template_name="core/index.html")
