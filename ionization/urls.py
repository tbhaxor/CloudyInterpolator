from django.urls import path

from .views import DownloadFileView, Interpolation

app_name = 'ionization'
urlpatterns = [
    path('interpolation/', Interpolation.as_view(), name='interpolation'),
    path('download/<int:batch_id>/', DownloadFileView.as_view(), name='download')
]
