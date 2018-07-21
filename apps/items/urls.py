from django.conf.urls import url

from .views import ItemList, ItemDetail

urlpatterns = [
    # url(r'^brands/$', BrandList.as_view()),
    url(r'^items/$', ItemList.as_view()),
    url(r'^items/(?P<pk>[0-9]+)/$', ItemDetail.as_view()),
]
