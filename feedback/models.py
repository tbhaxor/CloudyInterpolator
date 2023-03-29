from django.db import models

# Create your models here.


class FeedbackModel(models.Model):
    email = models.EmailField(
        null=False,
        blank=False,
        default=None,
        verbose_name='Email Address',
        help_text='This will help us to reach you when we launch a new version of the application',
    )

    name = models.CharField(
        max_length=128,
        null=False,
        default=None,
        verbose_name='Full Name',
        help_text='This is how we will address you in the email',
    )

    message = models.TextField(
        null=False,
        blank=False,
        default=None,
        verbose_name='Message',
        help_text='Provide the feedback here',
    )

    created_at = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name='Created At',
        editable=False,
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f"{self.name}'s feedback"

    class Meta:
        get_latest_by = '-created_at'
        verbose_name = 'Feedback Submission'
        verbose_name_plural = f'{verbose_name}s'

    pass
