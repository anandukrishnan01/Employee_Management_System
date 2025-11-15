import json
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from base.functions import get_auto_id
from .models import FormTemplate


@login_required
def builder_view(request):
    return render(request, "forms/builder.html", {})


@login_required
def template_list(request):
    templates = FormTemplate.objects.filter(is_deleted=False)
    return render(request, "forms/template_list.html", {"templates": templates})


@login_required
def edit_template(request, slug):
    tmpl = get_object_or_404(FormTemplate, slug=slug)
    return render(request, "forms/builder.html", {"template": tmpl})


@login_required
def delete_template(request, slug):
    tmpl = get_object_or_404(FormTemplate, slug=slug)
    if request.method == "POST":
        tmpl.is_deleted = True
        tmpl.deleted_by = request.user
        tmpl.deleted_at = timezone.now()
        tmpl.save()
        return redirect("forms:template_list")
    return HttpResponseBadRequest("POST only")


@login_required
def save_template(request):
    # Accepts JSON body {name, description, schema, slug?}
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    name = payload.get("name")
    schema = payload.get("schema", [])
    description = payload.get("description", "")
    slug = payload.get("slug")
    if slug in ["null", "", None]:
        slug = None

    if not name or not isinstance(schema, list):
        return HttpResponseBadRequest("Invalid payload")

    if slug:
        tmpl = get_object_or_404(FormTemplate, slug=slug)
        tmpl.name = name
        tmpl.description = description
        tmpl.schema = schema
        tmpl.updated_by = request.user
        tmpl.save()
        created = False
    else:
        tmpl = FormTemplate.objects.create(
            name=name,
            description=description,
            schema=schema,
            created_by=request.user,
            auto_id=get_auto_id(FormTemplate)
        )
        created = True

    return JsonResponse({"status": "ok", "slug": tmpl.slug, "created": created})
