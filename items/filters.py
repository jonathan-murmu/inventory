import datetime

from django.contrib.auth.models import User
from rest_framework.filters import BaseFilterBackend

from items.constants import DATE_RANGE, USER_KEY


class NotificationFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = get_filters(request)
        if filters:
            return queryset.filter(**filters)
        else:
            return queryset


def get_filters(request):
    """Get the filters.

    Parses the query string and returns a dictionary to filter the queryset.
    Examples of date filter:
        http://domain/notifications/?d=2017-01-31_2017-10-3/
        or
        http://domain/articles/?d=2017-01-31_now/
    """
    main_filter = {}
    try:
        for key in request.query_params:
            # splitting the last '/' in the url
            value = request.query_params[key].split('/')[0]
            # filter by date range
            if key == DATE_RANGE:
                date_range = get_date_range_filter(value)
                main_filter['time__gte'] = date_range['from_date']
                main_filter['time__lte'] = date_range['to_date']
            # filter by user id
            elif key == USER_KEY:
                user_obj = User.objects.get(pk=value)
                main_filter['user'] = user_obj

    except:
        pass

    return main_filter


def get_date_range_filter(value):
    """Get the date range filter.

    Returns a dict with the date range filter.
    """
    from_date = value.split('_')[0]
    to_date = value.split('_')[1]
    if to_date.lower() in ['now']:
        to_date = datetime.datetime.now().strftime('%Y-%m-%d')

    value = {'from_date': from_date, 'to_date': to_date}

    return value