from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.v1.base.functions import create_response_data, generate_serializer_errors
from base.functions import get_auto_id
from .serializers import FormTemplateSerializer
from forms.models import FormTemplate


class FormTemplateListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        templates = FormTemplate.objects.filter(is_deleted=False)
        serializer = FormTemplateSerializer(templates, many=True)
        return Response(create_response_data(
            200, "Template List", serializer.data, {}, "Success"
        ))

    def post(self, request):
        serializer = FormTemplateSerializer(data=request.data)
        auto_id = get_auto_id(FormTemplate)
        if serializer.is_valid():
            serializer.save(created_by=request.user,auto_id=auto_id)
            return Response(create_response_data(
                201, "Template Created", serializer.data, {}, "Created Successfully"
            ))
        return Response(create_response_data(
            400, "Validation Error", {}, serializer.errors,
            generate_serializer_errors(serializer.errors)
        ), status=400)


class FormTemplateDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, slug):
        try:
            return FormTemplate.objects.get(slug=slug, is_deleted=False)
        except FormTemplate.DoesNotExist:
            return None

    def get(self, request, slug):
        template = self.get_object(slug)
        if not template:
            return Response(create_response_data(404, "Not Found", {}, {}, "Not Found"))
        serializer = FormTemplateSerializer(template)
        return Response(create_response_data(200, "Template Detail", serializer.data, {}, "Success"))

    def put(self, request, slug):
        template = self.get_object(slug)
        if not template:
            return Response(create_response_data(404, "Not Found", {}, {}, "Not Found"))

        serializer = FormTemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(create_response_data(200, "Updated", serializer.data, {}, "Updated Successfully"))
        return Response(create_response_data(
            400, "Validation Error", {}, serializer.errors,
            generate_serializer_errors(serializer.errors)
        ))

    def delete(self, request, slug):
        template = self.get_object(slug)
        if not template:
            return Response(create_response_data(404, "Not Found", {}, {}, "Not Found"))

        template.is_deleted = True
        template.deleted_by = request.user
        template.save()

        return Response(create_response_data(200, "Deleted", {}, {}, "Deleted Successfully"))
