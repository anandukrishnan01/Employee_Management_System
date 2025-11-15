import uuid

from rest_framework import serializers
from django.utils.text import slugify

from api.v1.base.serializers import BaseModelSerializer
from forms.models import FormTemplate


class FormTemplateSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = FormTemplate
        fields = BaseModelSerializer.COMMON_FIELDS + (
            "name", "slug", "description", "schema",
        )
        read_only_fields = BaseModelSerializer.COMMON_FIELDS + ("slug",)

    # Fix: ensure schema always has ID
    def _ensure_ids(self, schema):
        new_schema = []
        for f in schema:
            if not f.get("id"):
                f["id"] = "f_" + uuid.uuid4().hex[:8]
            new_schema.append(f)
        return new_schema

    def validate(self, attrs):
        name = attrs.get("name")
        instance = getattr(self, "instance", None)

        if instance:
            if FormTemplate.objects.exclude(id=instance.id).filter(name=name).exists():
                raise serializers.ValidationError({"name": "Form name already exists"})
        else:
            if FormTemplate.objects.filter(name=name).exists():
                raise serializers.ValidationError({"name": "Form name already exists"})
        return attrs

    def create(self, validated_data):
        # force id creation
        validated_data["schema"] = self._ensure_ids(validated_data.get("schema", []))

        base = slugify(validated_data["name"])
        slug = base
        counter = 1
        while FormTemplate.objects.filter(slug=slug).exists():
            slug = f"{base}-{counter}"
            counter += 1

        validated_data["slug"] = slug
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # force id creation on update too
        if "schema" in validated_data:
            validated_data["schema"] = self._ensure_ids(validated_data["schema"])

        return super().update(instance, validated_data)
