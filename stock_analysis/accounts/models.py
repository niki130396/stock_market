from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class StockMarketUser(models.Model):
    ACCOUNT_TYPES = [
        (1, 'Standard User'),
        (2, 'Paid User')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPES, default=ACCOUNT_TYPES[0][0])


@receiver(post_save, sender=User)
def post_save_create_custom_user(sender, instance, created, **kwargs):
    if created:
        StockMarketUser.objects.create(user=instance)
