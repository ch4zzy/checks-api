import os
import json
import pytest
from django.conf import settings
from moto import mock_s3
from apps.reciept.models import Check
from reciept.constants import StatusType
from reciept.utils import create_pdf



@pytest.mark.django_db
def test_create_pdf(mock_s3_bucket, check_order_data, check):
    check = check
    check.order = check_order_data["order"]
    check.save()
    check.refresh_from_db()
    create_pdf(check.id, check.check_type, check.order)
    check.refresh_from_db()
    assert check.status == StatusType.RENDERED

    expected_pdf_filename = f"{check.order['order_id']}_{check.check_type}.pdf"
    assert check.pdf_file.name.endswith(expected_pdf_filename)

    s3_file_key = f"media/{check.order['order_id']}_{check.check_type}.pdf"
    obj = mock_s3_bucket.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_file_key)
    assert obj["ContentType"] == "application/pdf"


    temp_html_file_path = os.path.join(settings.BASE_DIR, "tmp", f"{check.order['order_id']}_{check.check_type}.html")
    assert not os.path.exists(temp_html_file_path)