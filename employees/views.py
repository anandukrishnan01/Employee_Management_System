import json

from django.db import transaction
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from base.functions import get_auto_id
from .models import EmployeeRecord
from forms.models import FormTemplate


@login_required
def employee_list(request):
    q = request.GET.get('q', '').strip().lower()
    tpl = request.GET.get('template', '').strip()

    qs = EmployeeRecord.objects.select_related('template').filter(is_deleted=False).order_by('-created_at')
    if tpl:
        qs = qs.filter(template__slug=tpl)

    # naive in-Python filtering for small datasets (ok for machine test)
    if q:
        qs = [e for e in qs if q in ' '.join(map(str, e.data.values())).lower()]

    templates = FormTemplate.objects.filter(is_deleted=False)
    return render(request, "employees/employee_list.html", {
        "employees": qs,
        "templates": templates,
        "query": request.GET.get('q', ''),
        "sel_template": tpl,
    })


@login_required
def employee_create(request, slug):
    template = get_object_or_404(FormTemplate, slug=slug)
    return render(request, "employees/employee_form.html", {
        "template": template,
        "mode": "create",
        "record": None,
    })


@login_required
def employee_update(request, pk):
    record = get_object_or_404(EmployeeRecord, pk=pk, is_deleted=False)
    template = record.template

    record_json = json.dumps(record.data or {})
    schema_json = json.dumps(template.schema or [])

    return render(request, "employees/employee_form.html", {
        "template": template,
        "record": record,
        "schema_json": schema_json,
        "record_json": record_json,
        "mode": "update",
    })


@login_required
@require_POST
def employee_save(request, slug):
    template = get_object_or_404(FormTemplate, slug=slug)
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    data = payload.get("data", {})
    # simple required validation
    errors = {}
    for f in template.schema:
        if f.get("required") and not data.get(f["id"]):
            errors[f["id"]] = "required"
    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    # create employee with auto_id in a transaction
    with transaction.atomic():
        new_auto = get_auto_id(EmployeeRecord)
        emp = EmployeeRecord.objects.create(
            template=template,
            data=data,
            created_by=request.user,
            auto_id=new_auto
        )
    return JsonResponse({"ok": True, "id": emp.id})


@login_required
@require_POST
def employee_save_update(request, pk):
    record = get_object_or_404(EmployeeRecord, pk=pk, is_deleted=False)
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    data = payload.get("data", {})
    errors = {}
    for f in record.template.schema:
        if f.get("required") and not data.get(f["id"]):
            errors[f["id"]] = "required"
    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    record.data = data
    record.updated_by = request.user
    record.updated_at = timezone.now()
    record.save()
    return JsonResponse({"ok": True, "id": record.id})


@login_required
@require_POST
def employee_delete(request, pk):
    record = get_object_or_404(EmployeeRecord, pk=pk, is_deleted=False)
    record.is_deleted = True
    record.deleted_by = request.user
    record.deleted_at = timezone.now()
    record.save()
    return JsonResponse({"ok": True})
