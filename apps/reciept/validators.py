from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.reciept.models import Check, Printer


def validate_printers(point_id):
    """
    Validate the existence of printers with the specified point_id.
    """
    
    printers = Printer.objects.filter(point_id=point_id)
    if not printers.exists():
        raise ValidationError(
            "Printers with the specified point_id do not exist.", 
            code=status.HTTP_404_NOT_FOUND
        )


def validate_order(order_id):
    """
    Validate the uniqueness of the order_id in checks.
    """

    if Check.objects.filter(order__contains={"order_id": order_id}).exists():
        raise ValidationError(
            "Check with the specified order_id already exists.",
            code=status.HTTP_400_BAD_REQUEST,
        )


def validate_pdf(check_id):
    """
    Validate the PDF file of a check.
    """

    check = Check.objects.get(id=check_id)
    if not check.pdf_file:
        raise ValidationError(
            "The PDF file of the check has not been created yet.",
            code=status.HTTP_404_NOT_FOUND,
        )
