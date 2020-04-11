from django.urls import path
from . import views

urlpatterns = [
	path('',views.HomeNoMemberView.as_view(),name='home'),
    path('member/',views.HomeMemberView.as_view(),name='home_member'),
	path('member/vocabulary/add', views.translationform, name='add'),
    path('member/vocabulary/list', views.TranslationListView.as_view(), name='list_translations'),
    path('member/books/add', views.addbookform, name='add_book'),
    path('member/books/list', views.BooksListView.as_view(), name='list_book'),
    path('member/books/list/<str:slug>', views.BookView.as_view(), name='details_book'),
    path('member/books/list/<str:slug>/add-word', views.translationform, name='add_word_book'),
]