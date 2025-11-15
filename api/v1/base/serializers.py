from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    COMMON_FIELDS = (
        'id', 'auto_id', 'created_by', 'updated_by', 'deleted_by',
        'created_at', 'updated_at', 'deleted_at', 'is_deleted',
        'custom_order', 'alt_txt',
    )

    auto_id = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        abstract = True

    def get_auto_id(self, instance):
        return instance.auto_id if instance else ""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        excluded_fields = [
            'deleted_by',
            'deleted_at'
        ]
        for field in excluded_fields:
            data.pop(field, None)
        return data
