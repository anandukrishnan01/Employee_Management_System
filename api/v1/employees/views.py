from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.base.functions import create_response_data, generate_serializer_errors
from base.functions import get_auto_id
from .serializers import EmployeeSerializer
from employees.models import EmployeeRecord


class EmployeeListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = EmployeeRecord.objects.filter(is_deleted=False)
        serializer = EmployeeSerializer(records, many=True)
        return Response(create_response_data(
            200, "Employee List", serializer.data, {}, "Success"
        ))

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        auto_id = get_auto_id(EmployeeRecord)
        if serializer.is_valid():
            emp = serializer.save(created_by=request.user,auto_id=auto_id)
            return Response(create_response_data(
                201, "Employee Created", EmployeeSerializer(emp).data, {}, "Created Successfully"
            ))
        return Response(create_response_data(
            400, "Validation Error", {}, serializer.errors,
            generate_serializer_errors(serializer.errors)
        ))


class EmployeeDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return EmployeeRecord.objects.get(pk=pk, is_deleted=False)
        except EmployeeRecord.DoesNotExist:
            return None

    def get(self, request, pk):
        emp = self.get_object(pk)
        if not emp:
            return Response(create_response_data(404, "Not Found", {}, {}, "Not Found"))
        return Response(create_response_data(
            200, "Employee Detail", EmployeeSerializer(emp).data, {}, "Success"
        ))

    def put(self, request, pk):
        emp = self.get_object(pk)
        if not emp:
            return Response(create_response_data(404, "Not Found", {}, {}, "Not Found"))

        serializer = EmployeeSerializer(emp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(create_response_data(
                200, "Employee Updated", serializer.data, {}, "Updated Successfully"
            ))
        return Response(create_response_data(
            400, "Validation Error", {}, serializer.errors,
            generate_serializer_errors(serializer.errors)
        ))

    def delete(self, request, pk):
        emp = self.get_object(pk)
        if not emp:
            return Response(create_response_data(404, "Not Found", {}, {}, "Not Found"))

        emp.is_deleted = True
        emp.deleted_by = request.user
        emp.save()

        return Response(create_response_data(
            200, "Deleted", {}, {}, "Employee Deleted Successfully"
        ))
