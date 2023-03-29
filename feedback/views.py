from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

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
        self.success_url += f"?name={form.cleaned_data.get('name')}"
        return super().form_valid(form)

    pass


class FeedbackThankYouView(TemplateView):
    template_name = "feedback/thank-you.html"

    def get(self, request, *args, **kwargs):
        kwargs["name"] = request.GET.get("name")
        if kwargs["name"] is None:
            return redirect(reverse_lazy("feedback:submit"))
        return super().get(request, *args, **kwargs)
