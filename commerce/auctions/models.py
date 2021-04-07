from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime as dt


class AuctionListing(models.Model):
    img = models.CharField()
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    startingPrice = models.DecimalField(decimal_places=2)
    auctionStarts = models.DateTimeField(auto_now_add=True, auto_now=False)
    auctionEnds = models.DurationField()
    


class Bid(models.Model):
    offer = models.DecimalField(decimal_places=2)
    buyer = models.ManyToManyField(User, blank=False, related_name="offers")
    seller = models.ManyToManyField(User, blank=False, related_name="proposals")
    date = models.DateTimeField(auto_now_add=True, auto_now=False)



class Comment(models.Model):
    content = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    author = models.ManyToManyField(User, blank=False, related_name="comment")
    auction = models.ManyToManyField(AuctionListings, blank=False, related_name="comment")


class User(AbstractUser):
    pass
