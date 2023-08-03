from django.urls import path

from apps.reciept.views import CheckCreate, CheckDetail, CheckList, CheckUpdate

app_name = "reciept"


urlpatterns = [
    path("check/", CheckList.as_view(), name="check-list"),
    path("check/<int:pk>/", CheckDetail.as_view(), name="check-detail"),
    path("check/create/", CheckCreate.as_view(), name="check-create"),
    path("check/<int:pk>/update/", CheckUpdate.as_view(), name="check-update"),
]
