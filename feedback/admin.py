from django.contrib import admin

from .models import FeedbackModel


# Register your models here.
@admin.register(FeedbackModel)
class FeedbackSiteAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
