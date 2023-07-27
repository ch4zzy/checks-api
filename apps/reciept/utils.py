import json
import os

import boto3
import pdfkit
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from apps.reciept.constants import StatusType
from apps.reciept.models import Check
from config.settings import BASE_DIR, PDFKIT_CONFIG


def create_pdf(id, check_type, order_detail):
    """
    Create a PDF file for a check and save it to the media/pdf directory.
    """

    check = Check.objects.get(id=id)
    order_id = order_detail["order_id"]
    # os.path.join(BASE_DIR, "media/pdf")

    # Generate the HTML template for the check
    check_template = render_to_string(
        "reciept/pdf_template.html", context={"order_id": order_id, "order_detail": json.dumps(order_detail)}
    )

    # Save the HTML template to a temporary file
    html_file_path = os.path.join(BASE_DIR, "tmp", f"{order_id}_{check_type}.html")
    with open(html_file_path, "w") as file:
        file.write(check_template)

    # Convert the HTML template to a PDF file using pdfkit
    pdf_data = pdfkit.from_file(html_file_path, False, configuration=PDFKIT_CONFIG)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    s3_file_key = f"media/{order_id}_{check_type}.pdf"
    s3.upload_fileobj(ContentFile(pdf_data), settings.AWS_STORAGE_BUCKET_NAME, s3_file_key)

    pdf_url = f"{order_id}_{check_type}.pdf"
    check.pdf_file = pdf_url

    # Remove the temporary HTML file
    os.remove(html_file_path)

    # Update status
    check.status = StatusType.RENDERED
    check.save(update_fields=["status"])
    check.save(update_fields=["pdf_file"])

    return None
