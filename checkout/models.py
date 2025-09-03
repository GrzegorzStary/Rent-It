import uuid
from decimal import Decimal
from datetime import timedelta

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField
from items.models import Product
from profiles.models import Profile 


class Order(models.Model):
    order_number = models.CharField(
        max_length=32, null=False, editable=False
    )
    user_profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders'
    )
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    country = CountryField(blank_label='Country *')
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)

    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        help_text="Optional fuel/delivery fee (e.g., for local delivery)"
    )
    deposit_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0,
        help_text="Security deposit total"
    )
    site_fee = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0,
        help_text="Platform fee (10% of rental total)"
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0,
        help_text="Rental subtotal (excluding deposit/site fee)"
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0,
        help_text="Final total including delivery, deposit, site fee"
    )

    original_checkout = models.TextField(
        default='', help_text="Snapshot of the checkout session at the time of order"
    )
    stripe_pid = models.CharField(max_length=254, default='')

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_use', 'In Use'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ]
    order_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )

    notes = models.TextField(blank=True, null=True)

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added or removed.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or Decimal('0.00')

        total = self.order_total

        if self.delivery_cost:
            total += self.delivery_cost

        total += (self.deposit_total or Decimal('0.00'))
        total += (self.site_fee or Decimal('0.00'))

        self.grand_total = total
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='lineitems'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )

    start_date = models.DateField()
    end_date = models.DateField()
    rental_duration = models.PositiveIntegerField(
        help_text="Duration in days", default=1
    )

    lineitem_total = models.DecimalField(
        max_digits=9, decimal_places=2,
        null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Set lineitem total based on product price * duration
        and update order totals.
        """
        if not self.rental_duration:
            self.rental_duration = (self.end_date - self.start_date).days or 1

        price = Decimal(str(self.product.price)) if self.product.price else Decimal('0.00')
        self.lineitem_total = (price * Decimal(self.rental_duration)).quantize(Decimal('0.01'))

        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f'{self.product.name} on order {self.order.order_number}'
