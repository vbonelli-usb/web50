from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:id>", views.single, name="single"),
    path("close", views.close_auction, name="close"),
    path("watch", views.watch_auction, name="watch"),
    path("watchlist", views.watchlist, name='watchlist'),
    path("wins", views.wins, name='wins'),
    path("myauctions", views.my_auctions, name="myauctions"),
    path("comment", views.comment, name="comment")
]
