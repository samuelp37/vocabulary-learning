from django.urls import path
from . import views

urlpatterns = [
	path('',views.HomeNoMemberView.as_view(),name='home'),
    path('member/',views.HomeMemberView.as_view(),name='home_member'),
	path('member/vocabulary/add', views.CreateTranslationView.as_view(), name='add'),
    path('member/vocabulary/list', views.TranslationListView.as_view(), name='list_translations'),
    path('member/books/add', views.CreateBookView.as_view(), name='add_book'),
    path('member/books/update/<str:slug>', views.UpdateBookView.as_view(), name='update_book'),
    path('member/books/list', views.BooksListView.as_view(), name='list_book'),
    path('member/books/details/<str:slug>', views.BookView.as_view(), name='details_book'),
    path('member/books/details/<str:slug>/add-word', views.CreateTranslationView.as_view(), name='add_word_book'),
]