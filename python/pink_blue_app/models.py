from django.db import models

PENDING = 0
APPROVED = 1
STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
)


class Inventory(models.Model):
    product_name = models.CharField(max_length=250, blank=True, null=True)
    vendor = models.CharField(max_length=300, blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    batch_number = models.CharField(max_length=250, blank=True, null=True)
    batch_date = models.DateField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING, null=True, blank=True)

    def __str__(self):
        return self.id



