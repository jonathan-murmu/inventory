from django.conf.urls import url

from .views import ItemList, ItemDetail, NotificationList

urlpatterns = [
    url(r'^items/$', ItemList.as_view()),
    url(r'^items/(?P<pk>[0-9]+)/$', ItemDetail.as_view()),
    url(r'^notifications/$', NotificationList.as_view()),
]
