from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime as dt
from django.forms import ModelForm, DateTimeInput


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    img = models.CharField(max_length=200)
    title = models.CharField(max_length=40, name="Title")
    description = models.CharField(max_length=300)
    startingPrice = models.DecimalField(
        max_digits=9, decimal_places=2, name="Starting Price")
    auctionStarts = models.DateTimeField(
        auto_now_add=True, auto_now=False, name="Starts")
    auctionEnds = models.DateTimeField(name="Ends")

    def __str__(self):
        return f'{self.Title} #{self.id}'


class Bid(models.Model):
    offer = models.DecimalField(max_digits=9, decimal_places=2)
    auction = models.ManyToManyField(
        AuctionListing, blank=False, related_name="bid")
    buyer = models.ManyToManyField(User, blank=False, related_name="offers")
    seller = models.ManyToManyField(
        User, blank=False, related_name="proposals")
    date = models.DateTimeField(auto_now_add=True, auto_now=False)


class Comment(models.Model):
    content = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    author = models.ManyToManyField(User, blank=False, related_name="comment")
    auction = models.ManyToManyField(
        AuctionListing, blank=False, related_name="comment")


class CreateAuctionForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['Title', 'img', 'description', 'Starting Price', 'Ends']
        widgets = {
            'Ends':DateTimeInput(attrs={'type': 'datetime-local'}),
        }
