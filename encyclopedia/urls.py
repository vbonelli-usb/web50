from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="single"),
    # re_path(r'^search/(?P<q>)$', views.query, name='query')
    path("search", views.query, name="query")
]
