import uuid
from decimal import Decimal
from django_mysql.models import ListCharField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CharField

from django.conf import settings


class Bill(models.Model):
    vendor = models.CharField(max_length=50, null=False, blank=False)
    uuid_bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_ts = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    updated_ts = models.DateTimeField(auto_now=True, verbose_name='date updated')
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill_date = models.DateField(null=False, blank=False)
    due_date = models.DateField(null=False, blank=False)
    amount_due = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=10,
                                     validators=[MinValueValidator(Decimal('0.01'))])
    categories = ListCharField(base_field=CharField(max_length=10), size=6, max_length=(6 * 11))

    PAYMENT_STATS = [
        ('paid', 'paid'),
        ('due', 'due'),
        ('past_due', 'past_due'),
        ('no_payment_required', 'no_payment_required'),
    ]

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATS, verbose_name="paymentStatus")

    def __str__(self):
        return self.vendor
