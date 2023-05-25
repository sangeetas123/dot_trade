from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse


class Stock(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=3)
    currentPrice = models.IntegerField(default=0)

    def __str__(self):
        return self.name

'''
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
'''

class PurchasedStock(models.Model):
    stockId = models.ForeignKey(Stock, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    purchasedPrice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    lastUpdated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stockId.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(validators=[MaxLengthValidator(10),
                                           RegexValidator(r'^[a-zA-Z0-9\s.]+$',
                                                          'Only alphanumeric characters, spaces and full stops are allowed.')
                                           ]) # At the ORM level
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('comment_detail', args=[str(self.id)])

    def __str__(self):
        return self.comment




