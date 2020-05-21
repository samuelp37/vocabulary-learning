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
    
    path('member/articles/add', views.CreateUpdateArticleView.as_view(), name='add_article'),
    path('member/articles/update/<str:slug_article>', views.CreateUpdateArticleView.as_view(), name='update_article'),
    path('member/articles/list', views.ArticlesListView.as_view(), name='list_article'),
    path('member/articles/details/<str:slug_article>', views.ArticleView.as_view(), name='details_article'),
    path('member/articles/delete/<str:slug_article>', views.DeleteArticleView.as_view(), name='delete_article'),
    
    path('member/articles/details/<str:slug_article>/vocabulary/add', views.CreateUpdateTranslationView.as_view(), name='add_word_article'),
    path('member/articles/details/<str:slug_article>/vocabulary/update/<str:slug>', views.CreateUpdateTranslationView.as_view(), name='update_translation_article'),
    path('member/articles/details/<str:slug_article>/vocabulary/view/<str:slug>', views.TranslationView.as_view(), name='view_translation_article'),
    path('member/articles/details/<str:slug_article>/vocabulary/delete/<str:slug>', views.DeleteTranslationView.as_view(), name='delete_translation_article'),
    
    path('member/discussions/add', views.CreateUpdateDiscussionView.as_view(), name='add_discussion'),
    path('member/discussions/update/<str:slug_discussion>', views.CreateUpdateDiscussionView.as_view(), name='update_discussion'),
    path('member/discussions/list', views.DiscussionsListView.as_view(), name='list_discussion'),
    path('member/discussions/details/<str:slug_discussion>', views.DiscussionView.as_view(), name='details_discussion'),
    path('member/discussions/delete/<str:slug_discussion>', views.DeleteDiscussionView.as_view(), name='delete_discussion'),
    
    path('member/discussions/details/<str:slug_discussion>/vocabulary/add', views.CreateUpdateTranslationView.as_view(), name='add_word_discussion'),
    path('member/discussions/details/<str:slug_discussion>/vocabulary/update/<str:slug>', views.CreateUpdateTranslationView.as_view(), name='update_translation_discussion'),
    path('member/discussions/details/<str:slug_discussion>/vocabulary/view/<str:slug>', views.TranslationView.as_view(), name='view_translation_discussion'),
    path('member/discussions/details/<str:slug_discussion>/vocabulary/delete/<str:slug>', views.DeleteTranslationView.as_view(), name='delete_translation_discussion'),
    
    path('member/review/add', views.CreateReviewView.as_view(), name='add_review'),
    path('member/review/list', views.ReviewsListView.as_view(), name='list_reviews'),
    
    path('member/review/delete/<str:slug_review>', views.DeleteReviewView.as_view(), name='delete_review'),
    path('member/review/details/<str:slug_review>', views.ReviewView.as_view(), name='details_review'),
    # Recover previous session
    path('member/review/resume/<str:slug_review>', views.ResumeReviewView.as_view(), name='resume_review'),
    
    path('member/review/details/<str:slug_review>/review_item/<str:slug_item>', views.QuizzReviewItemView.as_view(), name='quizz_review_item'),
    path('member/review/details/<str:slug_review>/analysis_review_item/<str:slug_item>/<int:success>', views.QuizzAnalysisReviewItemView.as_view(), name='quizz_analysis_review_item'),
    
    path('ajax/autocomplete/word', views.WordAutocompleteView.as_view(), name='autocomplete_word'),
    path('ajax/autocomplete/adjective', views.AdjectiveAutocompleteView.as_view(), name='autocomplete_adj'),
    path('ajax/autocomplete/verb', views.VerbAutocompleteView.as_view(), name='autocomplete_verb'),
    path('ajax/autocomplete/author', views.AuthorAutocompleteView.as_view(), name='autocomplete_author'),
    path('ajax/autocomplete/newspaper', views.NewspaperAutocompleteView.as_view(), name='autocomplete_newspaper'),
    path('ajax/autocomplete/topic', views.TopicAutocompleteView.as_view(), name='autocomplete_topic'),
]