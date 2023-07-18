from django.test import TestCase
from apps.reciept.constants import RecieptType, StatusType


class ConstantsTestCase(TestCase):
    """
    Constants test cases.
    """

    def test_reciept_type_choices(self):
        """
        Test that the receipt type choices have the expected values.
        """
        self.assertEqual(RecieptType.KITCHEN, "kitchen")
        self.assertEqual(RecieptType.CLIENT, "client")

    def test_status_type_choices(self):
        """
        Test that the status type choices have the expected values.
        """
        self.assertEqual(StatusType.NEW, "new")
        self.assertEqual(StatusType.RENDERED, "rendered")
        self.assertEqual(StatusType.PRINTED, "printed")
