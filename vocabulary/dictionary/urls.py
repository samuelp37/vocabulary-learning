from django.urls import path
from . import views, views_common

urlpatterns = [
	path('',views.HomeNoMemberView.as_view(),name='home'),
    path('member/',views.HomeMemberView.as_view(),name='home_member'),
    
	path('member/vocabulary/add', views.CreateUpdateTranslationView.as_view(), name='add'),
    path('member/vocabulary/list', views.TranslationListView.as_view(), name='list_translations'),
    path('member/vocabulary/details/<str:slug>', views.TranslationView.as_view(), name='details_translation'),
    path('member/vocabulary/update/<str:slug>', views.CreateUpdateTranslationView.as_view(), name='update_translation'),
    path('member/vocabulary/delete/<str:slug>', views.DeleteTranslationView.as_view(), name='delete_translation'),
    
    path('member/books/add', views.CreateUpdateBookView.as_view(), name='add_book'),
    path('member/books/update/<str:slug_book>', views.CreateUpdateBookView.as_view(), name='update_book'),
    path('member/books/list', views.BooksListView.as_view(), name='list_book'),
    path('member/books/details/<str:slug_book>', views.BookView.as_view(), name='details_book'),
    path('member/books/delete/<str:slug_book>', views.DeleteBookView.as_view(), name='delete_book'),
    
    path('member/books/details/<str:slug_book>/vocabulary/add', views.CreateUpdateTranslationView.as_view(), name='add_word_book'),
    path('member/books/details/<str:slug_book>/vocabulary/update/<str:slug>', views.CreateUpdateTranslationView.as_view(), name='update_translation_book'),
    path('member/books/details/<str:slug_book>/vocabulary/view/<str:slug>', views.TranslationView.as_view(), name='view_translation_book'),
    path('member/books/details/<str:slug_book>/vocabulary/delete/<str:slug>', views.DeleteTranslationView.as_view(), name='delete_translation_book'),
    
    path('ajax/autocomplete/word', views.WordAutocompleteView.as_view(), name='autocomplete_word'),
    path('ajax/autocomplete/adjective', views.AdjectiveAutocompleteView.as_view(), name='autocomplete_adj'),
    path('ajax/autocomplete/verb', views.VerbAutocompleteView.as_view(), name='autocomplete_verb'),
    path('ajax/autocomplete/author', views.AuthorAutocompleteView.as_view(), name='autocomplete_author'),

]