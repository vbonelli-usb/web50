from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/single.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/not-found.html", {
            "title": title
        })
