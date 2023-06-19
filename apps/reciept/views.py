from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.reciept.constants import StatusType
from apps.reciept.models import Check, Printer
from apps.reciept.serializers import CheckListSerializer, CheckSerializer
from apps.reciept.tasks import async_create_pdf
from apps.reciept.validators import validate_order, validate_pdf, validate_printers


class CheckListViewSet(viewsets.ModelViewSet):
    serializer_class = CheckListSerializer
    queryset = Check.objects.all()

    @action(detail=True, methods=["get"])
    def printer_list(self, request, pk):
        """
        List of checks for printer.
        """

        printer = get_object_or_404(Printer, pk=pk)
        available_checks = printer.checks.all()
        serializer = self.get_serializer(available_checks, many=True)
        return Response(serializer.data)


class CheckViewSet(viewsets.GenericViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def create(self, request):
        data = request.data
        point_id = data.get("point_id")
        order_id = data.get("order", {}).get("order_id")

        validate_printers(point_id)
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


class RetrieveUpdateCheckViewSet(viewsets.GenericViewSet):
    """
    A view set for retrieving and updating checks, simulating check printing in a real case.
    """

    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def get_object(self):
        """
        Retrieve the check object based on the provided ID.
        """

        check_id = self.kwargs["pk"]
        return get_object_or_404(Check, id=check_id)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the PDF file of a printed check and mark its status as printed.
        """

        check = self.get_object()
        validate_pdf(check.id)

        file_path = check.pdf_file.path
        file_name = check.pdf_file.name.split("/")[-1]

        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        check.status = StatusType.PRINTED
        check.save()
        return response