# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from rest_framework import generics

from items import filters
from items.utils import GroupConcat
from .models import Item, Notification
from .serializers import ItemSerializer, NotificationSerializer


class ItemList(generics.ListCreateAPIView):
    """List all the Items or create a new item."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save(last_modified_by=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """Get/Update/Delete a single item."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_update(self, serializer):
        serializer.save(
            last_modified_by=self.request.user,
            variants__last_modified_by=self.request.user,
            variants__properties__last_modified_by=self.request.user
        )


class NotificationList(generics.ListAPIView):
    """List the Notification feed."""
    serializer_class = NotificationSerializer
    filter_backends = (filters.NotificationFilter,)

    def get_queryset(self):
        queryset = Notification.objects.values(
            'user__username', 'time', 'action', 'item'
        ).annotate(
            count=Count(1),
            fields=GroupConcat('field', ordering='time DESC', separator=' | ')
        ).order_by('-time', '-count')

        return queryset
