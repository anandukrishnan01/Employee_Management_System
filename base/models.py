import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    created_by = models.ForeignKey(
        "accounts.User", blank=True, null=True, related_name="created_by_%(class)s_objects", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        "accounts.User", blank=True, null=True, related_name="updated_by_%(class)s_objects", on_delete=models.CASCADE
    )
    deleted_by = models.ForeignKey(
        "accounts.User", blank=True, null=True, related_name="deleted_by_%(class)s_objects", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    deleted_at = models.DateTimeField(db_index=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    custom_order = models.BigIntegerField(null=True, blank=True)
    alt_txt = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        abstract = True
