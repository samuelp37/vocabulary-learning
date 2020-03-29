from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('vocabulary/add', views.translationform, name='add'),
    path('books/add', views.addbookform, name='add_book'),
#	path('lectures/list', views.LecturesListView.as_view(), name='lectures-list'),
]