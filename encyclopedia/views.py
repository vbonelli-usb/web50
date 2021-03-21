from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

from . import util
from . import entries


def create(request):
    form = entries.CreateForm()
    return render(request, "encyclopedia/create.html", {
        "form": form
    })


def wiki(request, title):

    entry = entries.matchEntry(title)

    return (
        render(request, "encyclopedia/single.html", {
            "title": title,
            "entry": entry
        })
        if entry else
        render(
            request,
            "encyclopedia/not-found.html",
            {
                "title": title
            },
            status=404
        )
    )


def query(request):

    query = request.GET['q']

    entryQuery = entries.matchEntry(query)

    return (
        HttpResponseRedirect(reverse("single", args=[query]))
        if entryQuery else
        entries.searchQueries(request, query)
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
