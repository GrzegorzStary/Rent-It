from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date',
        'order_total', 'deposit_total', 'site_fee',
        'grand_total', 'original_checkout',
        'stripe_pid',
    )

    fields = (
        'order_number', 'user_profile', 'date', 'full_name',
        'email', 'phone_number', 'country',
        'postcode', 'town_or_city', 'street_address1',
        'street_address2', 'county',
        'delivery_cost', 'deposit_total', 'site_fee',
        'order_total', 'grand_total',
        'original_checkout', 'stripe_pid',
        'order_status', 'notes',
    )

    list_display = (
        'order_number', 'date', 'full_name',
        'order_status', 'order_total',
        'deposit_total', 'site_fee', 'delivery_cost',
        'grand_total',
    )

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
