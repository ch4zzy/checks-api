import json
import os

import pdfkit
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
    os.path.join(BASE_DIR, "media/pdf")

    # Generate the HTML template for the check
    check_template = render_to_string(
        "reciept/pdf_template.html", context={"order_id": order_id, "order_detail": json.dumps(order_detail)}
    )

    # Save the HTML template to a temporary file
    html_file_path = os.path.join(BASE_DIR, "tmp", f"{order_id}_{check_type}.html")
    with open(html_file_path, "w") as file:
        file.write(check_template)

    # Convert the HTML template to a PDF file using pdfkit
    pdf_file_path = os.path.join(BASE_DIR, "media/pdf", f"{order_id}_{check_type}.pdf")
    pdfkit.from_file(html_file_path, pdf_file_path, configuration=PDFKIT_CONFIG)

    # Save the PDF file to the media/pdf directory
    with open(pdf_file_path, "rb") as file:
        check.pdf_file.save(os.path.join("pdf", f"{order_id}_{check_type}.pdf"), ContentFile(file.read()))

    # Remove the temporary HTML file
    os.remove(html_file_path)

    # Update status
    check.status = StatusType.RENDERED
    check.save(update_fields=["status"])

    return None
