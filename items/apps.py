# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from fieldsignals import pre_save_changed


class ItemsConfig(AppConfig):
    name = 'items'

    def ready(self):
        from .models import Item, Property, Variant
        from .signals import on_create_item, on_delete_item, \
            on_delete_property, on_delete_variant, \
            item_field_changes, property_field_changes, \
            variant_field_changes

        post_save.connect(on_create_item, sender=Item)
        post_delete.connect(on_delete_property, sender=Property)
        post_delete.connect(on_delete_variant, sender=Variant)
        post_delete.connect(on_delete_item, sender=Item)

        pre_save_changed.connect(item_field_changes, sender=Item)
        pre_save_changed.connect(variant_field_changes, sender=Variant)
        pre_save_changed.connect(property_field_changes, sender=Property)
