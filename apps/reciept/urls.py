from django.urls import path

from .views import CheckCreate, CheckDetail, CheckList, CheckRetrieveUpdate

app_name = "reciept"


urlpatterns = [
    path("check/", CheckList.as_view(), name="check-list"),
    path("check/<int:pk>/", CheckDetail.as_view(), name="check-detail"),
    path("check/create/", CheckCreate.as_view(), name="check-create"),
    path("check/<int:pk>/update/", CheckRetrieveUpdate.as_view(), name="check-update-retrieve"),
]
