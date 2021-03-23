from django import forms
from django.shortcuts import render, reverse
from django.template import Template, Context, Engine

import markdown2 as md
import re

from . import util


class EntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=30)
    content = forms.CharField(label="Content", widget=forms.Textarea)


def getEntryElements(entryMD):
    # entryHTML = md.markdown(entryMD)
    # matchEntry = re.match(r"<h1>(?P<title>.*)<\/h1>\n\n", entryHTML)
    matchEntry = re.match(r"#(?P<title>.*)\W*", entryMD)
    if matchEntry:
        title = matchEntry.group("title")
        content = entryMD[matchEntry.end():]
        return {
            "title": title,
            "content": content, }
    else:
        return None


def matchEntry(title):
    for entryTitle in util.list_entries():
        if re.match(f"^{title}$", entryTitle, re.IGNORECASE):
            return util.get_entry(entryTitle)

    return None


def searchQueries(request, query):
    results = []

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
