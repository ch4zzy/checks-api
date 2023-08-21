import pytest
from django.db.utils import IntegrityError
from apps.reciept.models import Printer, Check
from apps.reciept.constants import RecieptType, StatusType


@pytest.mark.django_db
def test_printer_creation():
    printer = Printer.objects.create(
        name="Test Printer",
        api_key="test_api_key",
        check_type=RecieptType.KITCHEN,
        point_id=1
    )
    assert printer.name == "Test Printer"
    assert printer.api_key == "test_api_key"
    assert printer.check_type == RecieptType.KITCHEN
    assert printer.point_id == 1


@pytest.mark.django_db
def test_unique_api_key():
    with pytest.raises(IntegrityError):
        Printer.objects.create(
            name="Printer 1",
            api_key="duplicate_key",
            check_type=RecieptType.KITCHEN,
            point_id=1
        )
        Printer.objects.create(
            name="Printer 2",
            api_key="duplicate_key",
            check_type=RecieptType.CLIENT,
            point_id=2
        )


@pytest.mark.django_db
def test_check_creation():
    printer = Printer.objects.create(
        name="Test Printer",
        api_key="test_api_key",
        check_type=RecieptType.KITCHEN,
        point_id=1
    )
    check = Check.objects.create(
        printer=printer,
        check_type=RecieptType.KITCHEN,
        order={"item": "Test Item"},
        status=StatusType.NEW
    )
    assert check.printer == printer
    assert check.check_type == RecieptType.KITCHEN
    assert check.order == {"item": "Test Item"}
    assert check.status == StatusType.NEW
