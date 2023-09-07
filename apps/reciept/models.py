from django.db import models

from .constants import RecieptType, StatusType


class Printer(models.Model):
    """
    Model representing a printer.
    """

    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=50, unique=True)
    check_type = models.CharField(max_length=10, choices=RecieptType.choices)
    point_id = models.IntegerField()


class Check(models.Model):
    """
    Model representing a check.
    """

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name="checks")
    check_type = models.CharField(max_length=10, choices=RecieptType.choices)
    order = models.JSONField()
    status = models.CharField(max_length=10, choices=StatusType.choices)
    pdf_file = models.FileField(blank=True)
