from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, DateTimeInput, HiddenInput
from django.core.validators import MinValueValidator
from .modelsview import is_auction_active, check_bid
import datetime as dt


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        'AuctionListing', related_name='watchers')

    def add_auction_to_watchlist(self, auction):
        self.watchlist.add(auction)


class AuctionListing(models.Model):
    img = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=40, name="Title")
    description = models.CharField(max_length=300)
    startingPrice = models.DecimalField(
        max_digits=9, decimal_places=2, name="Starting Price", validators=[MinValueValidator(0, message="Price can't be below zero (0)")])
    auctionStarts = models.DateTimeField(
        auto_now_add=True, auto_now=False, name="Starts")
    auctioneer = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, blank=False, related_name="auctions")
    is_active = models.BooleanField(
        default=True, null=False, blank=False, editable=False)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def get_highest_bid(self):
        bids = Bid.objects.filter(auction=self)

        if bids:
            return float(bids.order_by('-offer')[0].offer)

        return (float(getattr(self, 'Starting Price')))

    def __str__(self):
        return f'{self.Title} #{self.id}'


class Bid(models.Model):
    offer = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[check_bid])
    auction = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, default="", blank=False, related_name="bid", editable=False)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, default="", related_name="bids", editable=False)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"Bid of {self.offer}$ on {self.date}"

    def __call__(self):
        highest_bid = self.auction.get_highest_bid()
        if float(self.offer) > highest_bid:
            return True
        else:
            return False


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
                  'Starting Price', ]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['offer', ]

# class CloseAuctionForm(ModelForm):
#     class Meta:
#         model =
