from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class Transaction(models.Model):
    STATUS_CHOICES = (
        (1, _('Payment has not been made')),
        (2, _('Payment has failed')),
        (3, _('An error has occurred')),
        (4, _('blocked')),
        (5, _('Return to payer')),
        (6, _('Systemic backlash')),
        (7, _('Cancellation of payment')),
        (8, _('Moved to the payment gateway')),
        (10, _('Awaiting payment confirmation')),
        (100, _('Payment is confirmed')),
        (101, _('Payment has already been confirmed')),
        (200, _('It was deposited to the recipient')),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_('User')
    )
    order_id = models.CharField(
        max_length=50,
        verbose_name=_('Order ID')
    )
    transaction_id = models.CharField(
        max_length=255,
        verbose_name=_('Transaction ID')
    )
    amount = models.IntegerField(
        verbose_name=_('Amount')
    )
    date = models.DateTimeField(
        verbose_name=_('Date')
    )
    card_number = models.CharField(
        max_length=100,
        verbose_name=_('Card number')
    )
    gateway_track_id = models.IntegerField(
        verbose_name=_('Gateway track ID')
    )
    bank_track_id = models.CharField(
        max_length=100,
        verbose_name=_('Bank track ID')
    )
    status = models.IntegerField(
        verbose_name=_('Status')
    )


    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
