from django import template
from MainApp.models import Snippet
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm

register = template.Library()


def replace(code: str):
    return code.replace('\n', '<br>')


register.filter('replace', replace)


def lang_filter(request):
    if request.method == "POST":
        value = request.POST.get("lang_filter")
    snippets = Snippet.objects.filter(lang=value)
    counter = snippets.count
    context = {'pagename': 'Мои снипп', "snippets": snippets, "counter": counter}
    return render(request, 'pages/view_snippets.html', context)


def ID_filter(request):
        if request.method == "POST":
            value = request.POST.get("number")
        snippets = Snippet.objects.filter(pk=value)
        context = {'pagename': 'Cниппет', "snippets": snippets}
        return render(request, 'pages/view_snippets.html', context)



