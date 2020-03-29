from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('vocabulary/add', views.translationform, name='add'),
    path('vocabulary/list', views.TranslationListView.as_view(), name='list_translations'),
    path('books/add', views.addbookform, name='add_book'),
    path('books/list', views.BooksListView.as_view(), name='list_book'),
    path('books/list/<str:slug>', views.BookView.as_view(), name='details_book'),
    path('books/list/<str:slug>/add-word', views.translationform, name='add_word_book'),
]