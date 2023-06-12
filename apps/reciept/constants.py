from django.db import models


class RecieptType(models.TextChoices):
    """
    Choices for receipt types.
    """

    KITCHEN = "kitchen", "Kitchen"
    CLIENT = "client", "Client"


class StatusType(models.TextChoices):
    """
    Choices for receipt status types.
    """

    NEW = "new", "New"
    RENDERED = "rendered", "Rendered"
    PRINTED = "printed", "Printed"
