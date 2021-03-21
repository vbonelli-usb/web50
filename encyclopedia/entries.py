from django import forms
from django.shortcuts import render, reverse
import re

from . import util


class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=30)
    content = forms.CharField(label="Content", widget=forms.Textarea)


def matchEntry(title):
    for entryTitle in util.list_entries():
        if re.match(f"^{title}$", entryTitle, re.IGNORECASE):
            return util.get_entry(entryTitle)

    return None


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
