from django.urls import path

from .views import DownloadFileView, InterpolateView

app_name = 'emission'
urlpatterns = [
    path('interpolation/', InterpolateView.as_view(), name='interpolation'),
    path('download/<int:batch_id>/', DownloadFileView.as_view(), name='download')
]
