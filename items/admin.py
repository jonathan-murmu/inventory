# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib import admin

from .models import Item, Variant, Property, Notification

admin.site.register(Item)
admin.site.register(Variant)
admin.site.register(Property)
admin.site.register(Notification)