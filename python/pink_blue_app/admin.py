from django.contrib import admin

from pink_blue_app.models import Inventory


@admin.register(Inventory)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'vendor', 'mrp', 'batch_number', 'batch_date', 'quantity', 'status')
