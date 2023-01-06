from django.urls import path

from .views import DownloadFileView, InterpolateView

app_name = 'ionization'
urlpatterns = [
    path('interpolate/', InterpolateView.as_view(), name='interpolate'),
    path('download/<int:batch_id>/', DownloadFileView.as_view(), name='download')
]
