from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.reciept.views import (
    CheckListViewSet,
    CheckViewSet,
    RetrieveUpdateCheckViewSet,
)

app_name = "reciept"

router = DefaultRouter()

router.register(r"check", CheckListViewSet, basename="check")
router.register(r"create", CheckViewSet, basename="create")
router.register(r"checkfile", RetrieveUpdateCheckViewSet, basename="check-file")

urlpatterns = [
    path("", include(router.urls)),
]
