# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from items import filters
from .models import Item, Notification
from .serializers import ItemSerializer, NotificationSerializer


# class BrandList(generics.ListCreateAPIView):
#     sa = Session()
#     Brand = Brand.sa
#     queryset = sa.query(Brand).all()
#     serializer_class = BrandSerializer


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save(last_modified_by=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user,
                        variants__last_modified_by=self.request.user,
                        variants__properties__last_modified_by=self.request.user
        )


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = (filters.NotificationFilter,)
