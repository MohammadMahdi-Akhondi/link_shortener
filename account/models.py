from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email address'),
    )
    phone = models.CharField(
        max_length=11,
        unique=True,
        null=True, blank=True,
        verbose_name=_('Phone')
    )
    premium_until = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Premium up to'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def is_premium(self):
        """ is_premium for return premium status """
        if self.premium_to > timezone.now():
            return True
        return False

    is_premium.boolean = True
