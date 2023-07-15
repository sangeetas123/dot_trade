from django.core.validators import MaxLengthValidator, RegexValidator, MinLengthValidator

from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

from django.db.models.functions import Concat
from django.db.models import Value

from cryptography.fernet import Fernet

import binascii

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

class EncryptedField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fernet = Fernet(b'T3hzrNTA9mMrkL1-vu6IUEz3skymjBU1yxE_z-2oJZo=') #Idealy, pick from setttings

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.fernet.decrypt(value).decode('ascii')

    '''
    def to_python(self, value):
        if value is None:
            return value
        try:
            print("value ", value)
            return self.fernet.decrypt(value)
        except Exception as e:
            print("Exception ", e)
    '''

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value
        return self.fernet.encrypt(value.encode('utf-8'))

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.fernet.encrypt(value.encode('utf-8'))

class Profile(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20,
                                  validators=[RegexValidator(
                                      r'^[A-Za-z]+$', 'Only alphabets allowed')])
    last_name = models.CharField(max_length=20,
                                 validators=[RegexValidator(
                                     r'^[A-Za-z]+$', 'Only alphabets allowed')])
    credit_card = EncryptedField(editable=True, null=True)
    date_of_birth = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    save_payment_information = models.BooleanField(default=False)

    def __str__(self):
        return str(Concat('first_name', Value(' '), 'last_name'))


from django.db import models
from django.contrib.auth.models import User

class APIKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key

