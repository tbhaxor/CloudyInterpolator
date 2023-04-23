from django.urls import path

from .views import DownloadFileView, InterpolationView

app_name = "ionization"
urlpatterns = [
    path("interpolation/", InterpolationView.as_view(), name="interpolation"),
    path("download/<int:batch_id>/", DownloadFileView.as_view(), name="download"),
]
