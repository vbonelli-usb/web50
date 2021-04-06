from django.contrib.auth.models import AbstractUser
from django.db import models


class AuctionListings(models.Model):
    img = models.CharField()
    startingPrice = models.DecimalField(decimal_places=2)
    description = models.CharField(max_length=300)


class Bids(models.Model):
    offer = models.DecimalField(decimal_places=2)


class Comments(models.Model):
    content = models.TextField(max_length=400)
    author =


class User(AbstractUser):
    pass
