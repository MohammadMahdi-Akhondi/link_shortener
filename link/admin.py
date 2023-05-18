from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import Link


admin.site.site_header = _('Link Shortener Service')
admin.site.site_title = _('Link Shortener Service')
admin.site.index_title = _('Link Shortener Management')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'real_link',
    )
    search_fields = (
        'title',
        'real_link',
        'token',
        'description',
    )
    list_filter = (
        'is_active',
        'expire_at',
        'created_at'
    )
