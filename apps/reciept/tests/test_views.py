import pytest
from django.urls import reverse
from rest_framework import status
from apps.reciept.models import Printer, Check
from apps.reciept.constants import RecieptType, StatusType

@pytest.mark.django_db
class TestCheckViews:

    def test_check_list_view(self, client):
        """
        Test check list view.
        """
        url = reverse("api_reciept:check-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_check_detail_view(self, client, check_create):
        """
        Test check detail view.
        """
        check = check_create
        url = reverse("api_reciept:check-detail", kwargs={"pk": check.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_check_create_view(self, client, printer_create, check_order_data):
        """
        Test check create view.
        """
        printer = printer_create
        url = reverse("api_reciept:check-create")
        response = client.post(url, data=check_order_data, content_type="application/json", format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_check_retrieve_update_view(self, client, printer_create, check_data_pdf):
        """
        Test check retrieve and update view.
        """
        printer = printer_create
        check = Check.objects.create(**check_data_pdf)
        url = reverse("api_reciept:check-update-retrieve", kwargs={"pk": check.pk})

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = client.put(url, content_type="application/json")
        assert response.status_code == status.HTTP_302_OK
        check.refresh_from_db()
    
        assert check.status == StatusType.PRINTED
        assert check.pdf_file == "test.pdf"


