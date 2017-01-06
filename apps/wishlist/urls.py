from django.conf.urls import url
from . import views

app_name = 'wishlist'
urlpatterns = [
    url(r'^dashboard$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^remove$', views.remove, name='remove'),
    url(r'^addThis$', views.addThis, name='addThis'),
    url(r'^getItem/(?P<id>\d+)$', views.getItem, name='getItem'),
]
