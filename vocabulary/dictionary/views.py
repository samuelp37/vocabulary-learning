from django.shortcuts import render
from . import forms
from django.views.generic.list import ListView
#from .models import Lecture
from django.http import HttpResponse


def home(request):
    return HttpResponse('Hello, World!')

def translationform(request):
    form = None
    #if form is submitted
    if request.method == 'POST':
        #will handle the request later
        a = 0
    else:
        #creating a new form
        form = forms.TranslationForm()
        formA = forms.WordForm()
        formB = forms.WordForm()
        
    #returning form 
    return render(request, 'dictionary/vocform.html', {'form':form,'formA':formA,'formB':formB})

"""
class LecturesListView(ListView):

	model = Lecture
	paginate_by = 10  # if pagination is desired
	template_name = "dictionary/lectures_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
"""