from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

import re

from . import util
import markdown2 as md

# Module develeped to manipulate the entries data
from . import entries


def random(request):
    return HttpResponseRedirect(reverse("single", args=[entries.getRandomEntry()]))


def edit(request, title):
    errors = []

    if request.method == "POST":
        form = entries.EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if entries.matchEntry(title):
                content = re.sub(r"(\r\n){2,}", "\r\n", form.cleaned_data["content"])
                formattedContent = entries.formatContent(title, content)
                util.save_entry(title, formattedContent)
                return HttpResponseRedirect(reverse("single", args=[title]))
            else:
                return HttpResponseRedirect(reverse("create"))
        else:
            errors.append("No valid input")

    if request.method == "GET":
        entryRaw = entries.matchEntry(title)
        if entryRaw:
            entry = entries.getEntryElements(entryRaw)
            form = entries.EntryForm(
                initial=entry
            )
        else:
            return HttpResponseRedirect(reverse("create"))

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "errors": errors
    })
            


def create(request):
    errors = []
    if request.method == "POST":
        form = entries.EntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            if entries.matchEntry(title):
                status = 409
                errors.append(
                    """This entry have already been created.
                    You can edit in the article page.""")
            else:
                formattedContent = entries.formatContent(title, form.cleaned_data["content"])
                util.save_entry(
                    title,
                    formattedContent)
                return HttpResponseRedirect(reverse("single", args=[title]))

    if request.method == "GET":
        form = entries.EntryForm()
        status = 200

    return render(request, "encyclopedia/create.html", {
        "form": form,
        "errors": errors
    },
        status=status)


def wiki(request, title):

    entry = entries.matchEntry(title)

    return (
        render(request, "encyclopedia/single.html", {
            "title": title,
            "entry": md.markdown(entry)
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

    if query:

        entryQuery = entries.matchEntry(query)

        return (
            HttpResponseRedirect(reverse("single", args=[query]))
            if entryQuery else
            entries.searchQueries(request, query)
        )
    else:
        return HttpResponseRedirect(reverse("index"))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
