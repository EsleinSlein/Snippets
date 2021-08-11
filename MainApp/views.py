from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm ,UserRegistrationForm
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', "form": form}
        return render(request, 'pages/add_snippet.html', context)

    form = SnippetForm(request.POST)
    if form.is_valid():
        snippet = form.save(commit=False)
        if request.user.is_authenticated:
            snippet.user = request.user
        snippet.save()
        return redirect('list-snippet')
    context = {'pagename': 'Добавление нового сниппета', "form": form}
    return render(request, 'pages/add_snippet.html', context)


@login_required
def delete_snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    snippet.delete()
    return redirect('list-snippet')

def my_snippets(request):
    snippet = Snippet.objects.filter(user_id = request.user)
    snippets = snippet
    counter = snippets.count
    context = {'pagename': 'Мои сниппеты', "snippets": snippets, "counter": counter}
    return render(request, 'pages/view_snippets.html', context)


@login_required
def edit_snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    if request.method == "GET":
        context = {
            'pagename': 'Страница сниппета',
            "snippet": snippet,
            "edit": True
        }
        context.update(csrf(request))
        return render(request, 'pages/snippet-info.html', context)
    snippet.name = request.POST.get("name")
    snippet.code = request.POST.get("code")
    snippet.save()
    return redirect('list-snippet')


def snippets_page(request):
    snippets = Snippet.objects.all()
    counter = snippets.count
    if request.user.is_authenticated:
        snippets = Snippet.objects.all()

        context = {'pagename': 'Просмотр сниппетов', "snippets": snippets, "counter": counter}
        return render(request, 'pages/view_snippets.html', context)
    context = {'pagename': 'Просмотр сниппетов', "snippets": snippets, "counter": counter}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, id):
    snippet = Snippet.objects.get(pk=id)
    context = {'pagename': 'Страница сниппета', "snippet": snippet}
    return render(request, 'pages/snippet-info.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('Home')


def logout(request):
    auth.logout(request)
    return redirect('Home')


def register(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {"form": form}
        return render(request, 'pages/register_page.html', context)

    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('Home')
    context = {"form": form}
    return render(request, 'pages/register_page.html', context)