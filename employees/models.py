from django.db import models

from base.models import BaseModel
from forms.models import FormTemplate


class EmployeeRecord(BaseModel):
    template = models.ForeignKey(FormTemplate, on_delete=models.PROTECT, related_name='employee_records')
    data = models.JSONField(default=dict)

    class Meta:
        db_table = "employee_records"
        ordering = ["-created_at"]

    def __str__(self):
        name = self.data.get("name") or self.data.get("Name")
        return f"{name or self.auto_id}"
