from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import FeedbackSubmitView

app_name = "feedback"
urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("feedback:submit"))),
    path("submit/", FeedbackSubmitView.as_view(), name="submit"),
]
