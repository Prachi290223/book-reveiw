"""
URL configuration for book_review project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from books.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', book_details, name='book_details'),
    path('',book_list, name='book_list'),
    path("login/",login_page,name="login_page"),
    path("logout/",logout_page,name="logout_page"),
    path("register/",register,name="register"),

    path("add_books/",add_books,name="add_books"),
    path("edit_book/<id>",edit_book,name="edit_book"),
    path("delete_book/<id>",delete_book,name="delete_book"),
  
    path("add_review/<id>",add_review,name="add_review"),
    path("edit_review/<id>",edit_review,name="edit_review"),
    path("delete_review/<id>",delete_review,name="delete_review"),


]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+=staticfiles_urlpatterns()
