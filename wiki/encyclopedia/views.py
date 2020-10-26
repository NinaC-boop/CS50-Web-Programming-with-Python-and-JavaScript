from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
import random
import markdown2

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def page(request, title):
    if title not in util.list_entries():
        return render(request, "encyclopedia/404.html")

    content = util.get_entry(title)
    html = markdown2.markdown(content)
    return render(request, "encyclopedia/page.html", {
        "content": html,
        "title": title,
    })

# note: request.GET is a dictionary-like object containing all GET request parameters. The method get() returns a value for the given key if key is in the dictionary. If key is not available then returns default value None.  
def search_view(request):
    query = request.GET.get('q')
    list_entries = util.list_entries()

    if query in list_entries:
        return page(request, query)
    else:
        filtered_list_entries = []
        for entry in list_entries:
            if query.lower() in entry.lower():
                filtered_list_entries.append(entry) 

        return render(request, "encyclopedia/search_results.html", {
            "entries": filtered_list_entries,
            "query": query
        })

def new(request):
    if request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get('title')
        if title in util.list_entries():
            return render(request, "encyclopedia/101.html", {
                "title": title
            })
        else:
            util.save_entry(title, content)
            return page(request, title)

    return render(request, "encyclopedia/new.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get('content') 
        util.save_entry(title, content)
        return page(request, title)

    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

# note: don't use generic names or they'll overwrite
def rand(request):
    list_entries = util.list_entries()

    if list_entries == []:
        return render(request, "encyclopedia/404.html")

    title = random.choice(list_entries)
    return page(request, title)