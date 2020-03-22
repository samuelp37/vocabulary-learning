from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('vocabulary/add', views.vocform, name='add'),
	path('lectures/list', views.LecturesListView.as_view(), name='lectures-list'),
]