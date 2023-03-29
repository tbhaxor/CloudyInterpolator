from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView

from .views import FeedbackSubmitView, FeedbackThankYouView

app_name = "feedback"
urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("feedback:submit"))),
    path("submit", FeedbackSubmitView.as_view(), name="submit"),
    path("thank-you", FeedbackThankYouView.as_view(), name="thank-you"),
    re_path(r".*", RedirectView.as_view(url=reverse_lazy("feedback:submit"))),
]
