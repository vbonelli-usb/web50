from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render ,reverse

from . import util

import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def matchEntry(title):
    for entryTitle in util.list_entries():
        if re.match(f"^{title}$", entryTitle, re.IGNORECASE):
            return util.get_entry(entryTitle)

    return None

def wiki(request, title):

    entry = matchEntry(title)

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

def searchQueries(request, query):
    results = []

    for entryTitle in util.list_entries():
        if re.match(f".*{query}.*", entryTitle, re.IGNORECASE):
            results.append(util.get_entry(entryTitle))

    return render(
            request,
            "encyclopedia/no-match.html",
            {
                "title": query,
                "results": results
            },
            status=300
        )

def query(request, query):

    entryQuery = matchEntry(query)

    return (
        HttpResponseRedirect(reverse("single", args=[query])) 
        if entryQuery else 
        searchQueries(request, query)
    )
