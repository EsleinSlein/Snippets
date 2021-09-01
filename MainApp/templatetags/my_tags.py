from django import template
from MainApp.models import Snippet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
register = template.Library()


def pagination(request, snippets):
    paginator = Paginator(snippets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj



def replace(code: str):
    return code.replace('\n', '<br>')


register.filter('replace', replace)



def ID_filter(request):
        if request.method == "GET":
            id = request.GET.get("number")
        snippets = Snippet.objects.filter(pk=id)
        if not snippets.exists():
            messages.error(request, 'Сниппет не найден!')
            return redirect('Home')
        page_obj = pagination(request, snippets)
        context = {'pagename': 'Cниппет', "snippets": snippets, 'page_obj': page_obj}
        return render(request, 'pages/view_snippets.html', context)


