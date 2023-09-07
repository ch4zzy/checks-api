from django.contrib import admin

from .models import Check, Printer


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ("id", "printer", "check_type", "order", "status", "pdf_file")
    list_filter = (
        "check_type",
        "status",
    )


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_key", "check_type", "point_id")
    list_filter = ("check_type",)
