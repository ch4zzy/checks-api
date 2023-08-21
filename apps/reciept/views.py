from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from rest_framework import generics, status
from rest_framework.response import Response

from apps.reciept.constants import StatusType
from apps.reciept.models import Check, Printer
from apps.reciept.serializers import (
    CheckListSerializer,
    CheckSerializer,
    CheckUpdateSerializer,
)
from apps.reciept.tasks import async_create_pdf
from apps.reciept.validators import (
    validate_check_by_id,
    validate_order,
    validate_printers_by_point,
)


class CheckList(generics.ListAPIView):
    """
    List of checks for point_id.
    """

    serializer_class = CheckListSerializer
    queryset = Check.objects.all()

    def get_queryset(self):
        """
        Get the queryset for the list of checks.
        """

        queryset = super().get_queryset()
        point_id = self.request.query_params.get("point_id", None)
        
        if point_id is not None:
            validate_printers_by_point(point_id)
            queryset = queryset.filter(printer__point_id=point_id)
        return queryset


class CheckDetail(generics.RetrieveAPIView):
    """
    Retrieve a check instance.
    """

    serializer_class = CheckSerializer
    queryset = Check.objects.all()

    def get_queryset(self):
        """
        Get the queryset for retrieving the check instance.
        """

        pk = self.kwargs.get("pk")
        validate_check_by_id(pk)
        queryset = self.queryset.filter(pk=pk)
        return queryset


class CheckCreate(generics.CreateAPIView):
    """
    Create a check.
    """

    serializer_class = CheckSerializer
    queryset = Check.objects.all()

    def create(self, request):
        """
        Create a new check instance.
        """

        data = request.data

        point_id = data.get("point_id")
        order_id = data.get("order", {}).get("order_id")

        validate_printers_by_point(point_id)
        validate_order(order_id)

        printers = Printer.objects.filter(point_id=point_id)

        created_checks = []

        for printer in printers:
            data = {
                "printer": printer.id,
                "check_type": printer.check_type,
                "order": data["order"],
                "status": data.get("status", StatusType.NEW),
            }

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            check = serializer.save()
            created_checks.append(serializer.data)
            async_create_pdf.delay(check.id, printer.check_type, data["order"])
        return Response(created_checks, status=status.HTTP_201_CREATED)


class CheckRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Retrieve or Update the check instance, returns a file and marks the check as printed if updated.
    """

    serializer_class = CheckUpdateSerializer
    queryset = Check.objects.all()

    def get_object(self):
        """
        Get the check object based on the provided 'pk'.
        """

        pk = self.kwargs.get("pk")
        validate_check_by_id(pk)
        return get_object_or_404(Check, pk=pk)

    def get_pdf_file_response(self, instance):
        """
        Get the PDF file response of the check instance.
        """

        file_name = instance.pdf_file.name

        response = FileResponse(instance.pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={slugify(file_name)}.pdf"

        return response

    def perform_update(self, serializer):
        """
        Update the check instance and set the status to 'StatusType.PRINTED'.
        """

        instance = serializer.save(status=StatusType.PRINTED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the check instance and return the PDF file.
        """

        instance = self.get_object()
        self.get_serializer(instance)

        return self.get_pdf_file_response(instance)

    def update(self, request, *args, **kwargs):
        """
        Update the check instance and return the PDF file.
        """

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return redirect("reciept:check-update-retrieve", pk=instance.id)
