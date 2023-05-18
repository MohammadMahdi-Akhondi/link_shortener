from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class Link(models.Model):
    title = models.CharField(
        max_length=80,
        verbose_name=_('Title')
    )
    real_link = models.URLField(
        verbose_name=_('Real link')
    )
    token = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Token')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='links',
        verbose_name=_('User')
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name=_('Description')
    )
    clicks_count = models.IntegerField(
        default=0,
        verbose_name=_('Clicks count')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active?')
    )
    expire_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('Expire at')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated')
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('Is deleted')
    )

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def __str__(self):
        return self.title
