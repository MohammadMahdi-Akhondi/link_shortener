from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'order_id',
        'amount',
        'date',
        'status',
    )
    list_filter = (
        'status',
        'date',
    )
    search_fields = (
        'order_id',
        'transaction_id',
        'gateway_track_id',
        'bank_track_id',
    )
