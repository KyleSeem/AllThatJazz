from __future__ import unicode_literals

from django.db import models
from ..login_reg.models import User
from datetime import datetime, date

# Create your models here.
class ItemManager(models.Manager):
    def create(self, postData):
        alerts = []

        if len(postData['item']) < 1:
            alerts.append('Item cannot be left blank.')
        elif len(postData['item']) < 3:
            alerts.append('Item must be at least 3 characters in length.')

        if alerts:
            return (False, alerts)
        else:
            user = User.objects.get(id=int(postData['user']))
            # print ('USER:', user.id, user.name)
            item = Item.objects.create(user=user, item=postData['item'])
            # print ('ITEM:', item.user.name, item.item)
            wishlist = Wishlist.objects.create(this_user=user, item=item)
            # print('LIST:', wishlist.user.name, wishlist.item.item)
            return (True, 'success')

    def bridge_connections(self, postData):
        if not postData:
            return (False)
        else:
            user = User.objects.get(id=int(postData['user']))
            item = Item.objects.get(id=int(postData['item']))

            Wishlist.objects.create(this_user=user, item=item)
            return (True)

    def delete(self, postData):
        item = Item.objects.get(id=int(postData['item']))
        item.delete()
        return (True)

    def remove(self, postData):
        listItem = Wishlist.objects.get(id=int(postData['listItem']))
        # print (listItem.id, listItem.item.item, listItem.this_user.name)
        listItem.delete()
        return (True)

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    itemManager = ItemManager()
    objects = models.Manager()

class Wishlist(models.Model):
    this_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
