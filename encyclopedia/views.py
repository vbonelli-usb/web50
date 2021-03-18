from django.shortcuts import render

from . import util

import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):

    for entryTitle in util.list_entries():
        if re.match(title, entryTitle, re.IGNORECASE):
            entry = util.get_entry(entryTitle)
            return render(request, "encyclopedia/single.html", {
                "title": entryTitle,
                "entry": entry
            })

    return render(request, "encyclopedia/not-found.html", {
        "title": title
    })
