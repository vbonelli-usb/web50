from django import forms
from django.shortcuts import render, reverse

import markdown2 as md
import random as rd
import re

from . import util


class EntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=30)
    content = forms.CharField(label="Content", widget=forms.Textarea)

def getRandomEntry():
    entries = util.list_entries()
    entryID = rd.randint(0, len(entries) - 1)
    return entries[entryID]



def getEntryElements(entryMD):
    # entryHTML = md.markdown(entryMD)
    # matchEntry = re.match(r"<h1>(?P<title>.*)<\/h1>\n\n", entryHTML)
    matchEntry = re.match(r"# (?P<title>.*)\n*", entryMD)
    if matchEntry:
        title = matchEntry.group("title")
        content = entryMD[matchEntry.end():]
        return {
            "title": title,
            "content": content, }
    else:
        return None

def formatContent(title, content):
    return f"# {title}\n\n{content}"


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
