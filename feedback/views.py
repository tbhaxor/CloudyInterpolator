from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import FeedbackForm

# Create your views here.


class FeedbackSubmitView(CreateView):
    template_name = "feedback/submit.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("feedback:thank-you")

    def form_invalid(self, form: FeedbackForm):
        is_autofocus = False
        for name, field in form.fields.items():
            if name in form.errors:
                field.widget.attrs = {
                    "class": f"{field.widget.attrs.get('class', '')} is-invalid".strip(),
                    "autofocus": "true" if is_autofocus else "false",
                }
                is_autofocus = True
        return super().form_invalid(form)

    def form_valid(self, form: FeedbackForm):
        form.save()
        return render(self.request, self.template_name, {"name": form.cleaned_data["name"]})
