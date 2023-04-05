from django.db import models

# Create your models here.


class FeedbackModel(models.Model):
    email = models.EmailField(
        null=False,
        blank=False,
        default=None,
        verbose_name='Email Address',
        help_text='When we release a new edition of the program, this will make it easier for us to contact you.',
    )

    name = models.CharField(
        max_length=128,
        null=False,
        default=None,
        verbose_name='Full Name',
        help_text="We'll refer to you in the communication as such.",
    )

    message = models.TextField(
        null=False,
        blank=False,
        default=None,
        verbose_name='Message',
        help_text='Give your comments here.',
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
