from django.contrib.auth.models import User
from django.db import models


# class Brand(models.Model):
#     """Model to store the Brand."""
#     brand_name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.brand_name


class Item(models.Model):
    """Model to store the Item."""
    item_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.item_name


class Variant(models.Model):
    """Variant for the Item."""
    variant_name = models.CharField(max_length=255)
    selling_price = models.FloatField(default=0.0)
    cost_price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)

    item = models.ForeignKey(Item, related_name='variants')

    def __str__(self):
        return self.variant_name


class Property(models.Model):
    """Holds the property for the variant."""
    option = models.CharField(max_length=255)  # e.g. size, cloth, etc
    value = models.CharField(max_length=255)  # e.g. L, cotton, etc

    variant = models.ForeignKey(Variant, related_name='properties')

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.option + ': ' + self.value


class Notification(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    # field which is being added/modified/deleted.
    field = models.CharField(max_length=255)

    # item
    item = models.ForeignKey(Item)

    # user
    user = models.ForeignKey(User)

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.user.username, self.field,
                                    self.item.item_name)
