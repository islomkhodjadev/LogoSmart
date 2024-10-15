from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
import re
from django.core.exceptions import ValidationError


class NewUser(AbstractUser):
    phoneNumber = PhoneNumberField(region="UZ", unique=True)

    @property
    def has_paid(self):
        return self.payment.is_due_date_expired


from django.utils import timezone
from dateutil.relativedelta import relativedelta


class Payment(models.Model):
    user = models.OneToOneField(
        NewUser, on_delete=models.CASCADE, related_name="payment"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    type = models.PositiveIntegerField(choices=((1, 1), (2, 2), (3, 3)), default=1)

    @property
    def due_date(self):

        return self.created_at + relativedelta(months=self.type)

    @property
    def is_due_date_expired(self):
        return timezone.now() > self.due_date
