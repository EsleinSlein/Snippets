from django.http import Http404
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', "snippets": snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, id):
    snippet = Snippet.objects.get(pk=id)
    context = {'pagename': 'Страница сниппета', "snippet": snippet}
    return render(request, 'pages/snippet-info.html', context)

def form_data(request):
    if request.method == "POST":
        name = request.POST["name"]
        lang = request.POST["lang"]
        code = request.POST["code"]
        snippet = Snippet(name=name, lang=lang, code=code)
        snippet.save()
    return redirect('list-snippet')

def delete(request, id):
        snippet= Snippet.objects.get(pk=id)
        snippet.delete()
        return redirect('list-snippet')



def edit(request, id):
    try:
        snippet= Snippet.objects.get(pk=id)

        if request.method == "POST":
            snippet.name = request.POST.get("name")
            snippet.lang = request.POST.get("lang")
            snippet.code = request.POST.get("code")
            snippet.save()
            return redirect('list-snippet')
        else:
            context = {"snippet": snippet}
            return render(request, "pages/edit.html", context )
    except Snippet.DoesNotExist:
        return HttpResponseNotFound("<h2>Snippet not found</h2>")
