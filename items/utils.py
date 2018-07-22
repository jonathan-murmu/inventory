from django.db.models import Aggregate, CharField


def add_notification(item=None, field=None, action=None, user=None):
    """Add in Notification model.

    Add an entry to notification whenever a Item-variant-property is
    added/modified/deleted."""
    from .models import Notification
    Notification.objects.create(
        item=item, field=field, action=action, user=user)


class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'

    def __init__(self, expression, distinct=False, ordering=None,
                 separator=',', **extra):
        super(GroupConcat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            ordering=' ORDER BY %s' % ordering if ordering is not None else '',
            separator=' SEPARATOR "%s"' % separator,
            output_field=CharField(),
            **extra
        )
