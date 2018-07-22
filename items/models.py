from django.contrib.auth.models import User
from django.db import models


from django.db.models.signals import post_save
from fieldsignals import pre_save_changed

from .constants import CREATE, DELETE, MODIFY
from .signals import on_create_item, item_field_changes


class Item(models.Model):
    """Model to store the Item."""
    item_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True, blank=True)
    last_modified_by = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.item_name


class Variant(models.Model):
    """Variant for the Item."""
    variant_name = models.CharField(max_length=255)
    selling_price = models.FloatField(default=0.0)
    cost_price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)

    item = models.ForeignKey(Item, related_name='variants')
    last_modified_by = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.variant_name


class Property(models.Model):
    """Holds the property for the variant."""
    option = models.CharField(max_length=255)  # e.g. size, cloth, etc
    value = models.CharField(max_length=255)  # e.g. L, cotton, etc

    variant = models.ForeignKey(Variant, related_name='properties')
    last_modified_by = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.option + ': ' + self.value


class Notification(models.Model):
    ACTION_CHOICES = (
        (CREATE, 'created'),
        (DELETE, 'deleted'),
        (MODIFY, 'modified'),
    )

    time = models.DateTimeField(auto_now_add=True)

    # field which is being added/modified/deleted.
    field = models.CharField(max_length=255, null=True, blank=True)
    # action done on a field.
    action = models.CharField(choices=ACTION_CHOICES, max_length=1)
    # item
    item = models.CharField(max_length=255)
    # user
    user = models.ForeignKey(User)

    def __str__(self):
        return '{0} {1} {2} {3}'.format(
            self.user.username, self.ACTION_CHOICES[int(self.action)-1][1],
            self.item, self.field or '',
        )
