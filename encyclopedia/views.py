from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from . import util

import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def matchEntry(request, title):
    for entryTitle in util.list_entries():
        if re.match(title, entryTitle, re.IGNORECASE):
            entry = util.get_entry(entryTitle)
            return render(request, "encyclopedia/single.html", {
                "title": entryTitle,
                "entry": entry
            })

    return None

def wiki(request, title):

    entryQuery = matchEntry(request, title)

    return (
        entryQuery 
        if entryQuery else 
        render(
            request,
            "encyclopedia/not-found.html",
            {
                "title": title
            },
            status=404
        )
    )

def searchQuery(request, query):
    return render(
            request,
            "encyclopedia/no-match.html",
            {
                "title": query
            },
            status=404
        )

def query(request, query):

    entryQuery = matchEntry(request, query)

    return (
        entryQuery 
        if entryQuery else 
        searchQuery(request, query)
    )
