from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.core.files.storage import default_storage
from . import util
import random
import markdown2


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
        "title": title,
        "entry": markdown2.markdown(entry)
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
    return redirect('entry', title=query)


class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def newpage(request):

    if request.method =="POST":

        form = NewEntry(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            filename = f"entries/{title}.md"

            if default_storage.exists(filename):
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "message": "Error: Entry not saved, an entry by this title already exists."
                })
            util.save_entry(title, content)
            entry = util.get_entry(title)
            return redirect('entry', title=title)

        return render(request, "encyclopedia/newpage.html", {
            "form": form,
            "message": "Form not valid."
        })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewEntry()
    })

class Edit(forms.Form):
    edit_field = forms.CharField(label="",widget=forms.Textarea)

def edit(request, title):
    entry = util.get_entry(title)
    form = Edit(initial={'edit_field': entry})

    if request.method == "POST":
        form = Edit(request.POST)

        if form.is_valid():
            new_entry = form.cleaned_data["edit_field"]
            util.save_entry(title, new_entry)
            return redirect('entry', title=title)

        return render(request, "encyclopedia/edit.html", {
            "title":title,
            "form":form
        })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })

def random_entry(request):
    entries = util.list_entries()
    
    title = random.choice(entries)
    return redirect('entry', title=title)

