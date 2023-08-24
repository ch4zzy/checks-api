import pytest
from apps.reciept.models import Printer, Check


@pytest.fixture
def printer_data():
    return {
        "name": "test_name",
        "api_key": "test_api",
        "check_type": "client",
        "point_id": 1
    }


@pytest.fixture
def printer_data_same_api_key():
    return {
        "name": "test_name",
        "api_key": "test_api",
        "check_type": "client",
        "point_id": 2
    }


@pytest.fixture
def check_data(printer_create):
    return {
        "printer": printer_create,
        "check_type": "client",
        "order": {"item": "Test Item"},
        "status": "new",
        "pdf_file": None
    }


@pytest.fixture
def printer_create(printer_data):
    return Printer.objects.create(**printer_data)


@pytest.fixture
def check_create(check_data, printer_create):
    return Check.objects.create(**check_data)
