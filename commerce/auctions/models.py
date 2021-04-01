from django.contrib.auth.models import AbstractUser
from django.db import models


class AuctionListings(models.Model):
    img = models.CharField()
    price = models.DecimalField(decimal_places=2)
    description = models.CharField(max_length=300)


class User(AbstractUser):
    pass
