from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="single"),
    path(r"search\?q=", views.query, name="query")
]
