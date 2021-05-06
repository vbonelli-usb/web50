from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment, CreateAuctionForm


def index(request):
    return render(request, "auctions/index.html", {
        'auctions': AuctionListing.objects.all()
    })


def single(request, id):
    auction = AuctionListing.objects.get(id=id)
    return render(request, "auctions/single.html", {
        'auction': auction,
    })


@login_required(login_url='login')
def bid(request):
    if request.method == "POST":
        # auction = AuctionListing.objects.get(id=)
        # bid_made = Bid(auction=, buyer=get_user(request))
        print(request.get_full_path())
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/nobid.html", status=400)


@login_required(login_url='login')
def create(request):
    auction = AuctionListing()
    auction.auctioneer.set(get_user(request))
    form = CreateAuctionForm(request.POST or None, instance=auction)
    if request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/create.html", {
            "form": form
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
