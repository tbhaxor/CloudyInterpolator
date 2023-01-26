from django.urls import path

from .views import DownloadFileView, InterpolateView

app_name = 'ionization'
urlpatterns = [
    path('download/', InterpolateView.as_view(), name='get-download-batch'),
    path('download/<int:batch_id>/', DownloadFileView.as_view(), name='download')
]
