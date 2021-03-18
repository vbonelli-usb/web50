from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="single"),
    path("search/<str:query>", views.query, name="query")
]
