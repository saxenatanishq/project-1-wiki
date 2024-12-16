from django.shortcuts import render
from . import util
from django.http import HttpResponse
import markdown2
from django import forms
import random

class searchform(forms.Form):
    name = forms.CharField(label = "search name")

class newform(forms.Form):
    title = forms.CharField(label = "title")
    details = forms.CharField(label = "details")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchform()
    })

def find(request):
    if request.method == "POST":
        form = searchform(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            list1 = []
            flag = 0
            for entry in util.list_entries():
                if name.lower() in entry.lower():
                    list1.append(entry)
                if name == entry:
                    flag = 1
            if flag == 1:
                markdown_content = util.get_entry(name)
                html_content = markdown2.markdown(markdown_content)
                return render(request, "encyclopedia/markdown_template.html",{
                    "html_content":html_content,
                    "name":name,
                    "form": searchform()
                })
            else:
                if len(list1) == 0:
                    return render(request, "encyclopedia/not_found.html", {
                        "entries": util.list_entries(),
                        "form": searchform(),
                        "name":name,
                        "code":1
                    })
                else:
                    return render(request, "encyclopedia/search_result.html", {
                        "entries": list1,
                        "form": searchform()
                    })

def greet(request, name):
    if util.get_entry(name) == None:
        return render(request, "encyclopedia/not_found.html", {
            "entries": util.list_entries(),
            "form": searchform(),
            "name":name,
            "code":0
        })
    else:
        markdown_content = util.get_entry(name)
        html_content = markdown2.markdown(markdown_content)
        return render(request, "encyclopedia/markdown_template.html",{
            "html_content":html_content,
            "name":name,
            "form":searchform()
        })

def add(request):
    return render(request,"encyclopedia/new.html",{
        "form": searchform(),
        "form1": newform()
    })

def new(request):
    if request.method == "POST":
        form = newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            details = form.cleaned_data["details"]
            for entry in util.list_entries():
                if title == entry:
                    return render(request, "encyclopedia/error.html",{
                        "form":searchform(),
                        "title":title
                    })
            util.save_entry(title, details)
            markdown_content = util.get_entry(title)
            html_content = markdown2.markdown(markdown_content)
            return render(request, "encyclopedia/markdown_template.html",{
                "html_content":html_content,
                "name":title,
                "form":searchform()
            })
            
def randomf(request):
    name = random.choice(util.list_entries())
    markdown_content = util.get_entry(name)
    html_content = markdown2.markdown(markdown_content)
    return render(request, "encyclopedia/markdown_template.html",{
        "html_content":html_content,
        "name":name,
        "form":searchform()
    })

def edit(request,name):
    markdown_content = util.get_entry(name)
    return render(request,"encyclopedia/edit.html",{
        "form": searchform(),
        "form1": newform(),
        "title1":name,
        "markdown_content":markdown_content
    })

def editf(request):
    if request.method == "POST":
        form = newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            details = form.cleaned_data["details"]
            util.save_entry(title, details)
            markdown_content = util.get_entry(title)
            html_content = markdown2.markdown(markdown_content)
            return render(request, "encyclopedia/markdown_template.html",{
                "html_content":html_content,
                "name":title,
                "form":searchform()
            })