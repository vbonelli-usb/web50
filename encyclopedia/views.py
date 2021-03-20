from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render ,reverse
from django import forms

from . import util

import re

class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=30)
    content = forms.CharField(label="Content", widget=forms.Textarea)

def create(request):
    form = CreateForm()
    return render(request, "encyclopedia/create.html", {
        "form": form
    })

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

    if query != "":
        for entryTitle in util.list_entries():
            if re.match(f".*{query}.*", entryTitle, re.IGNORECASE):
                results.append({
                    "content": util.get_entry(entryTitle),
                    "title": entryTitle})

        return render(
                request,
                "encyclopedia/no-match.html",
                {
                    "query": query,
                    "results": results
                },
                status=300
            )
    else:
        return HttpResponseRedirect(reverse("index"))

def query(request):

    query = request.GET['q']

    entryQuery = matchEntry(query)

    return (
        HttpResponseRedirect(reverse("single", args=[query])) 
        if entryQuery else 
        searchQueries(request, query)
    )
