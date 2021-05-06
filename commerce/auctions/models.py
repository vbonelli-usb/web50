from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime as dt
from django.forms import ModelForm, DateTimeInput, HiddenInput


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    img = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=40, name="Title")
    description = models.CharField(max_length=300)
    startingPrice = models.DecimalField(
        max_digits=9, decimal_places=2, name="Starting Price")
    auctionStarts = models.DateTimeField(
        auto_now_add=True, auto_now=False, name="Starts")
    auctionEnds = models.DateTimeField(name="Ends")
    auctioneer = models.ForeignKey(
        User, on_delete=models.CASCADE, default="", blank=False, related_name="auctions")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.Title} #{self.id}'


class Bid(models.Model):
    offer = models.DecimalField(max_digits=9, decimal_places=2)
    auction = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, default="", blank=False, related_name="bid", editable=False)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, default="", related_name="bids", editable=False)
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
        fields = ['Title', 'img', 'description',
                  'Starting Price', 'Ends', 'auctioneer', 'is_active']
        widgets = {
            'Ends': DateTimeInput(attrs={'type': 'datetime-local'}),
            'auctioneer': HiddenInput()
        }


class BidForm(ModelForm):
    class Meta:
        models = Bid
        fields = ['offer', ]
