from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if request.method == "POST":
        query = request.POST.get('q')
        entry = util.get_entry(query)
        entries = util.list_entries()
        if entry == None:
            results = []
            for i in entries:
                if query.lower() in i.lower():
                    results.append(i)
            return render(request, "encyclopedia/entry.html", {
                "title": "Search Results",
                "entry": results
            })
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "entry": entry
        })
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title.capitalize()
    })
