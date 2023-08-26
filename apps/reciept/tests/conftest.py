import pytest
from apps.reciept.models import Printer, Check
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from moto import mock_s3
import boto3


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
        "pdf_file": ""
    }


@pytest.fixture
def check_data_pdf(printer_create):
    pdf_content = b"PDF content"
    uploaded_pdf = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")

    return {
        "printer": printer_create,
        "check_type": "client",
        "order": {"item": "Test Item"},
        "status": "new",
        "pdf_file": uploaded_pdf
    }


@pytest.fixture
def check_order_data():
    return {
        "point_id": 1,
        "order": {
            "order_id": 1,
            "item": "Milk",
            "quantity": 2,
            "price": 10.99
        }
    }


@pytest.fixture
def printer_create(printer_data):
    return Printer.objects.create(**printer_data)


@pytest.fixture
def check_create(check_data, printer_create):
    return Check.objects.create(**check_data)


@pytest.fixture
def mock_s3_bucket():
    with mock_s3():
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
           # region_name=settings.AWS_S3_REGION_NAME,
        )
        s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        yield s3
