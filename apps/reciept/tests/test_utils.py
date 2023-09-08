import os
import json
import pytest
from django.conf import settings
from moto import mock_s3
from ..models import Check
from ..constants import StatusType
from ..utils import create_pdf
from dynamic_preferences.registries import global_preferences_registry


@pytest.mark.django_db
def test_create_pdf(mock_s3_bucket, check_order_data, check):
    check = check
    check.order = check_order_data["order"]
    check.save()
    check.refresh_from_db()
    create_pdf(check.id, check.check_type, check.order)
    check.refresh_from_db()
    assert check.status == StatusType.RENDERED

    global_preferences = global_preferences_registry.manager()
    company_name = global_preferences["company__company_name"]
    file_name = f"{company_name}_{check.order['order_id']}_{check.check_type}.pdf"

    expected_pdf_filename = file_name
    assert check.pdf_file.name.endswith(expected_pdf_filename)

    s3_file_key = f"media/{file_name}"
    obj = mock_s3_bucket.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_file_key)
    assert obj["ContentType"] == "application/pdf"


    temp_html_file_path = os.path.join(settings.BASE_DIR, "tmp", f"{company_name}_{check.order['order_id']}_{check.check_type}.html")
    assert not os.path.exists(temp_html_file_path)