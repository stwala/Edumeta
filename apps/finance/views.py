from django.shortcuts import render

from apps.accounts.decorators import role_required


@role_required("admin", "parent")
def index(request):
    return render(
        request,
        "finance/index.html",
        {"page_title": "Finance", "active_section": "finance"},
    )
