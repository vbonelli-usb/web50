from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, DateTimeInput, HiddenInput
from django.core.validators import MinValueValidator
from .modelsview import is_auction_active, check_bid
import datetime as dt


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    img = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=40, name="Title")
    description = models.CharField(max_length=300)
    startingPrice = models.DecimalField(
        max_digits=9, decimal_places=2, name="Starting Price", validators=[MinValueValidator(0, message="Price can't be below zero (0)")])
    auctionStarts = models.DateTimeField(
        auto_now_add=True, auto_now=False, name="Starts")
    auctionEnds = models.DateTimeField(name="Ends", validators=[is_auction_active])
    auctioneer = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, blank=False, related_name="auctions")

    def get_highest_bid(self):
        bids = Bid.objects.filter(auction=self)
        
        if bids:
            return int(bids.order_by('offer'.desc())[0])

        return self.startingPrice
        # query_set = self.bid.objects.order_by('offer'.desc())
        # return query_set[0].offer

    def __str__(self):
        return f'{self.Title} #{self.id}'


class Bid(models.Model):
    offer = models.DecimalField(max_digits=9, decimal_places=2, validators=[check_bid])
    auction = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, default="", blank=False, related_name="bid", editable=False)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, default="", related_name="bids", editable=False)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"Bid of {self.offer}$ on {self.date}"


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
                  'Starting Price', 'Ends',]
        widgets = {
            'Ends': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['offer', ]
