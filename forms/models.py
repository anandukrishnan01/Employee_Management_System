import json

from django.db import models
from django.utils.text import slugify

from base.models import BaseModel


class FormTemplate(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    schema = models.JSONField(default=list)

    class Meta:
        db_table = "form_templates"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_schema_json(self):
        return json.dumps(self.schema)

    def __str__(self):
        return self.name
