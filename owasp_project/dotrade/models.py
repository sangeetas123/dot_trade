from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=3)
    currentPrice = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PurchasedStock(models.Model):
    stockId = models.ForeignKey(Stock, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    purchasedPrice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    lastUpdated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stockId.name




