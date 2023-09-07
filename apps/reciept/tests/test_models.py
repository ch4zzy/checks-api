import pytest
from django.db.utils import IntegrityError
from reciept.models import Printer, Check


@pytest.mark.django_db
def test_printer_creation(printer, printer_data):
    assert Printer.objects.count() == 1
    printer = printer
    assert printer.name == printer_data["name"]
    assert printer.api_key == printer_data["api_key"]
    assert printer.check_type == printer_data["check_type"]
    assert printer.point_id == printer_data["point_id"]


@pytest.mark.django_db
def test_unique_api_key(printer, printer_data_same_api_key):
    with pytest.raises(IntegrityError):
        Printer.objects.create(**printer_data_same_api_key)


@pytest.mark.django_db
def test_check_creation(check_data, check):
    assert Check.objects.count() == 1
    assert Printer.objects.count() == 1
    check = check
    assert check.printer == check_data["printer"]
    assert check.check_type == check_data["check_type"]
    assert check.order == check_data["order"]
    assert check.status == check_data["status"]
