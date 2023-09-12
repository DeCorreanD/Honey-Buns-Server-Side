from django.db import models
from .item import Item
from .user import User

class FavoriteItem(models.Model):

    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
