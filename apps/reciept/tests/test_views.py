import pytest
from django.urls import reverse
from rest_framework import status
from ..models import Printer, Check
from ..constants import RecieptType, StatusType


@pytest.mark.django_db
class TestCheckViews:

    def test_check_list_view(self, client):
        """
        Test check list view.
        """
        url = reverse("api_reciept:check-list")
        response = client.get(url)
        assert response.status_code == 200

    def test_check_detail_view(self, client, check):
        """
        Test check detail view.
        """
        check = check
        url = reverse("api_reciept:check-detail", kwargs={"pk": check.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_check_view(self, client, printer, check_order_data):
        """
        Test check create view.
        """
        printer = printer
        url = reverse("api_reciept:check-create")
        response = client.post(url, data=check_order_data, content_type="application/json", format="json")
        assert response.status_code == 201

    def test_check_retrieve_update_view(self, client, printer, check_data_pdf):
        """
        Test check retrieve and update view.
        """
        printer = printer
        check = Check.objects.create(**check_data_pdf)
        url = reverse("api_reciept:check-update-retrieve", kwargs={"pk": check.pk})

        response = client.get(url)
        assert response.status_code == 200

        response = client.put(url, content_type="application/json")
        assert response.status_code == 302
        check.refresh_from_db()
    
        assert check.status == StatusType.PRINTED
        assert check.pdf_file == "test.pdf"


