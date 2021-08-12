"""Snippets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from MainApp import views
from MainApp.templatetags import my_tags



urlpatterns = [
    path('', views.index_page, name="Home"),
    path('snippets/add', views.add_snippet_page, name="add-snippet"),
    path('snippet/<int:id>', views.snippet, name="snippet-page"),
    path('snippets/list', views.snippets_page, name="list-snippet"),
    path('snippets/my_list', views.my_snippets, name="my_list-snippet"),
    path('snippet/delete/<int:id>', views.delete_snippet_page, name="snippet-delete"),
    path('snippet/edit/<int:id>', views.edit_snippet_page, name="snippet-edit"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('comment/add', views.comment_add, name="comment_add"),
    path('snippet/ID_filter', my_tags.ID_filter, name="ID_filter"),
    path('snippet/lang_filter', my_tags.lang_filter, name="lang_filter"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


