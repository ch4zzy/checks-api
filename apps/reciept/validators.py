from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.reciept.models import Check, Printer


def validate_printers(point_id):
    printers = Printer.objects.filter(point_id=point_id)
    if not printers.exists():
        raise ValidationError("Printers with the specified point_id do not exist.")


def validate_order(order_id):
    if Check.objects.filter(order__contains={"order_id": order_id}).exists():
        raise ValidationError("Check with the specified order_id already exists.")


def validate_pdf(check_id):
    check = Check.objects.get(id=check_id)
    if not check.pdf_file:
        raise status.HTTP_404_NOT_FOUND
