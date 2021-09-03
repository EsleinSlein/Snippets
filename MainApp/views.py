from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.template.context_processors import csrf
from django.contrib import auth,  messages
from django.contrib.auth.decorators import login_required
from MainApp.templatetags.my_tags import pagination
from django.contrib.auth.models import User
from django.db.models import Count




def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
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
        messages.success(request, 'Сниппет успешно создан!')
        return redirect('my_list-snippet')
    context = {'pagename': 'Добавление нового сниппета', "form": form}
    return render(request, 'pages/add_snippet.html', context)


@login_required
def delete_snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    if snippet.user != request.user:
        raise HttpResponseForbidden
    snippet.delete()
    return redirect('my_list-snippet')


@login_required
def edit_snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    form = SnippetForm(instance=snippet)
    if request.method == "GET":
        context = {
            'pagename': 'Страница сниппета',
            "snippet": snippet,
            "edit": True,
            "form": form
        }
        context.update(csrf(request))
        return render(request, 'pages/snippet-info.html', context)
    snippet.name = request.POST.get("name")
    snippet.code = request.POST.get("code")
    public = request.POST.get("public")
    if public == "on":
        public = "True"
        snippet.public = public
        snippet.save()
        return redirect(f'/snippet/{snippet.id}')
    public = "False"
    snippet.public = public
    snippet.save()
    return redirect(f'/snippet/{snippet.id}')


def my_snippets(request):
    fields = {"id": 0, "name": 0, "creation_date": 0}
    snippets = Snippet.objects.filter(user_id=request.user)
    lang_filter = request.POST.get("lang_filter")
    if request.method == "POST":
        snippets = Snippet.objects.filter(user_id=request.user).filter(lang=lang_filter)
    sort_field = request.GET.get("sort")
    if sort_field is not None:
        if "-" in sort_field:
            fields[sort_field.replace("-", "")] = 2
        else:
            fields[sort_field] = 1
        snippets = snippets.order_by(sort_field)
    page_obj = pagination(request, snippets)
    counter = snippets.count
    context = {'pagename': 'Мои сниппеты', 'describe': 'все ваши', "snippets": snippets, "counter": counter, 'page_obj': page_obj, "fields": fields}
    return render(request, 'pages/view_snippets.html', context)


def snippets_page(request):
    fields = {"id": 0, "name": 0, "creation_date": 0}
    snippets = Snippet.objects.filter(public=True)
    users = User.objects.all().annotate(count_snippets=Count('snippet'))
    users = [user for user in users if user.count_snippets > 0]
    lang_filter = request.POST.get("lang_filter")
    if lang_filter:
        snippets = Snippet.objects.filter(public=True).filter(lang=lang_filter)
    sort_user = request.GET.get("user")
    if sort_user:
        snippets = snippets.filter(user__username=sort_user)
    sort_field = request.GET.get("sort")
    if sort_field is not None:
        if "-" in sort_field:
            fields[sort_field.replace("-", "")] = 2
        else:
            fields[sort_field] = 1
        snippets = snippets.order_by(sort_field)
    page_obj = pagination(request, snippets)
    counter = snippets.count

    context = {'pagename': 'Просмотр сниппетов',
               "snippets": snippets,
               "counter": counter,
               "users": users,
               'page_obj': page_obj,
               'describe': 'все публичные',
               "fields": fields,
               }
    return render(request, 'pages/view_snippets.html', context)
    if request.user.is_authenticated:
        return snippets_page(request)





def snippet(request, id):
    snippet = Snippet.objects.get(pk=id)
    form_comment = CommentForm()
    context = {'pagename': 'Страница сниппета', "snippet": snippet, 'form_comment':form_comment}
    return render(request, 'pages/snippet-info.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            messages.error(request, 'Пользователь не найден!')
            return redirect('Home')
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
        messages.success(request, 'Пользователь успешно создан!')
        return redirect('Home')
    context = {"form": form}
    return render(request, 'pages/register_page.html', context)

@login_required
def comment_add(request):
    if request.method == "POST":
        form_comment = CommentForm(request.POST,request.FILES)
        snippet_id = request.POST["snippet_id"]
        if form_comment.is_valid():
            snippet = Snippet.objects.get(id= snippet_id)
            comment = form_comment.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
        return redirect(f'/snippet/{snippet_id}')
    raise Http404





@login_required
def comment_delete(request, id):
    comment = Comment.objects.get(pk=id)
    if comment.author != request.user:
        raise HttpResponseForbidden
    comment.delete()
    return redirect(f'/snippet/{comment.snippet_id}')

