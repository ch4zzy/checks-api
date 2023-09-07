from rest_framework import serializers

from .models import Check, Printer


class CheckSerializer(serializers.ModelSerializer):
    """
    Serializer for the Check model.
    """

    class Meta:
        model = Check
        fields = (
            "id",
            "printer",
            "check_type",
            "order",
            "status",
            "pdf_file",
        )


class CheckListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Check model. Simple view.
    """

    class Meta:
        model = Check
        fields = (
            "id",
            "check_type",
            "status",
        )


class CheckUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Check model. Update view.
    """

    class Meta:
        model = Check
        fields = (
            "id",
            "status",
        )


class PrinterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Printer model.
    """

    class Meta:
        model = Printer
        fields = (
            "id",
            "name",
            "api_key",
            "check_type",
            "point_id",
        )
