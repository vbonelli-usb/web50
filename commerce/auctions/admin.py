from django.contrib import admin
from .models import Bid, Comment, AuctionListing, User


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("Title", "id", "Starts", "Starting Price")


# Register your models here.
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(AuctionListing, AuctionAdmin)
admin.site.register(User)
