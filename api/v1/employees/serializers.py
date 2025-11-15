from rest_framework import serializers

from api.v1.base.serializers import BaseModelSerializer
from employees.models import EmployeeRecord
from forms.models import FormTemplate


class EmployeeSerializer(BaseModelSerializer):
    template_slug = serializers.CharField(write_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = EmployeeRecord
        fields = BaseModelSerializer.COMMON_FIELDS + (
            "template", "template_slug", "data",
        )
        read_only_fields = BaseModelSerializer.COMMON_FIELDS + ("template",)

    def validate(self, attrs):
        slug = attrs.get("template_slug")
        template = FormTemplate.objects.filter(slug=slug, is_deleted=False).first()

        if not template:
            raise serializers.ValidationError({"template_slug": "Template not found"})

        attrs["template"] = template  # attach template model instance

        # validate dynamic form fields
        data = attrs.get("data", {})
        errors = {}

        for field in template.schema:
            fid = field.get("id")
            if field.get("required") and not data.get(fid):
                errors[fid] = "This field is required"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        # remove write-only field so .create() won't receive it
        validated_data.pop("template_slug", None)

        return EmployeeRecord.objects.create(**validated_data)
