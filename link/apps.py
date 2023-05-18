from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class LinkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'link'
    verbose_name = _('Link management')
