# Generated by Django 4.1.7 on 2023-03-06 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dotrade', '0002_remove_purchasedstock_currentprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedstock',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
