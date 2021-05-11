from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment, CreateAuctionForm, BidForm


def index(request):
    return render(request, "auctions/index.html", {
        'auctions': AuctionListing.objects.all()
    })


def single(request, id):
    auction = AuctionListing.objects.get(id=id)
    user = get_user(request)
    bid = Bid(auction=auction, buyer=user)
    bid_form = BidForm(request.POST or None, instance=bid)
    
    if (request.method == 'POST'):
        # bid.offer = int(request.POST['offer'])
        # bid_form.offer = int(bid_form.offer)
        print(bid_form)
        if bid_form.is_valid():
            return HttpResponseRedirect(reverse('index'))
    
    return render(request, "auctions/single.html", {
        'auction': auction,
        'form':bid_form
    })


@login_required(login_url='login')
def create(request):
    auction = AuctionListing(auctioneer=get_user(request))
    form = CreateAuctionForm(request.POST or None, instance=auction)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))

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
