from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

from . import util
import markdown2 as md

# Module develeped to manipulate the entries data
from . import entries


def edit(request, title):
    entry = entries.matchEntry(title)

    # if entry:
    #     form = entries.EntryForm(
    #         initial={
    #             "content": entry
    #         }
    #     )
    return HttpResponse(entry)


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
                util.save_entry(
                    title,
                    form.cleaned_data["content"])
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
