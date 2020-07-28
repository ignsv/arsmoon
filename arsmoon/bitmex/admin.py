from django.contrib import admin

from arsmoon.bitmex.models import Order, Account


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderID',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', )
