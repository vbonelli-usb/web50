from django import forms
from . import models


def CreateAuctionForm(forms.ModelForm):
    class Meta:
        model = models.AuctionListing
        fields = ['img', 'Title', 'description', 'Starting Price']
