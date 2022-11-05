from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.core.files.storage import default_storage
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):

    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/entry.html", {
            "title": "Error",
            "entry": "Error 404: Requested page not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": entry
    })

def search(request):
    
    query = request.POST.get('q')
    entry = util.get_entry(query)
    entries = util.list_entries()

    if entry == None:
        results = []
        for i in entries:
            if query.lower() in i.lower():
                results.append(i)
        return render(request, "encyclopedia/search.html", {
            "title": "Search Results",
            "results": results
        })

    return render(request, "encyclopedia/entry.html", {
        "title": query.capitalize(),
        "entry": entry
    })


class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def newpage(request):

    if request.method =="POST":
        
        message = ""

        form = NewEntry(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            filename = f"entries/{title}.md"

            if default_storage.exists(filename):
                message = "Error: An entry by this title already exists."
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "message": message
                })

            util.save_entry(title, content)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": entry
            })

        return render(request, "encyclopedia/newpage.html", {
            "form": form
        })
        
    return render(request, "encyclopedia/newpage.html", {
        "form": NewEntry()
    })
        
