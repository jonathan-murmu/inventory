import datetime


def add_notification(item=None, field=None, action=None, user=None):
    from .models import Notification
    Notification.objects.create(
        item=item, field=field, action=action, user=user)
