from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.reciept.models import Check, Printer


def validate_printers_by_point(point_id: int) -> None:
    """
    Validate the existence of printers with the specified point_id.
    """

    printers = Printer.objects.filter(point_id=point_id)
    if not printers.exists():
        raise ValidationError(
            "Printers with the specified point_id do not exist.", code=status.HTTP_404_NOT_FOUND
        )


def validate_printer_by_id(printer_id: int) -> None:
    """
    Validate the existence of a printer with the specified id.
    """

    if not Printer.objects.filter(id=printer_id).exists():
        raise ValidationError(
            "Printer with the specified id does not exist.", code=status.HTTP_404_NOT_FOUND
        )


def validate_check_by_id(check_id: int) -> None:
    """
    Validate the existence of a check with the specified id.
    """

    if not Check.objects.filter(id=check_id).exists():
        raise ValidationError("Check with the specified id does not exist.", code=status.HTTP_404_NOT_FOUND)


def validate_order(order_id: int) -> None:
    """
    Validate the uniqueness of the order_id in checks.
    """

    if Check.objects.filter(order__contains={"order_id": order_id}).exists():
        raise ValidationError(
            "Check with the specified order_id already exists.",
            code=status.HTTP_400_BAD_REQUEST,
        )


def validate_pdf(check_id: int) -> None:
    """
    Validate the PDF file of a check.
    """

    check = get_object_or_404(Check, id=check_id)
    if not check.pdf_file:
        raise ValidationError(
            "The PDF file of the check has not been created yet.",
            code=status.HTTP_404_NOT_FOUND,
        )
