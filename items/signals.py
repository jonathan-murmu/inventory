from .constants import CREATE, MODIFY, DELETE
from .utils import add_notification


def on_create_item(sender, instance, created, **kwargs):
    if created:
        print ('Item is created,')
        add_notification(item=instance, field=None, action=CREATE,
                         user=instance.last_modified_by)


def on_delete_property(sender, instance, **kwargs):
    print 'property deleted'
    add_notification(item=instance, field=None, action=DELETE,
                     user=instance.last_modified_by)


def on_delete_variant(sender, instance, **kwargs):
    add_notification(item=instance, field=None, action=DELETE,
                     user=instance.last_modified_by)


def on_delete_item(sender, instance, **kwargs):
    add_notification(item=instance, field=None, action=DELETE,
                     user=instance.last_modified_by)


def item_field_changes(sender, instance, changed_fields=None,
                       **kwargs):
    for field, (old, new) in changed_fields.items():
        if field.name in ['last_modified_by', 'id']:
            continue
        print "%s changed from %s to %s" % (field.name, old, new)

        add_notification(item=instance, field=field.name, action=MODIFY,
                         user=instance.last_modified_by)


def variant_field_changes(sender, instance, changed_fields=None,
                          **kwargs):
    for field, (old, new) in changed_fields.items():
        if field.name in ['last_modified_by', 'id']:
            continue

        print "%s changed from %s to %s" % (field.name, old, new)

        add_notification(item=instance.item, field=field.name, action=MODIFY,
                         user=instance.last_modified_by)


def property_field_changes(sender, instance, changed_fields=None,
                           **kwargs):
    for field, (old, new) in changed_fields.items():
        if field.name in ['last_modified_by', 'id']:
            continue

        print "%s changed from %s to %s" % (field.name, old, new)

        add_notification(item=instance.variant.item, field=field.name, action=MODIFY,
                         user=instance.last_modified_by)
