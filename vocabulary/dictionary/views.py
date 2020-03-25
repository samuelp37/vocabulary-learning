from django.shortcuts import render
from . import forms
from django.views.generic.list import ListView
from . import models
from django.http import HttpResponse


def home(request):
    return HttpResponse('Hello, World!')
"""
class Entry:
    
    def __init__(word,article,lng):
        self.word = word
        self.article = article
        self.lng = lng
"""
def translationform(request):
    form = None
    #if form is submitted
    if request.method == 'POST':
        #will handle the request later
        a = 0
    else:
        #creating a new form
        form = forms.TranslationForm()
        formA = forms.WordForm(prefix="original")
        formB = forms.WordForm(prefix="translate")
        
        #words = models.Word.objects.all()
        words = {0:"word",1:"wordb"}
        #words = {0:{"word","article","lng"},1:{"wordb","articleb","lngb"}}
        print(words)
        
    #returning form 
    return render(request, 'dictionary/vocform.html', {'form':form,'formA':formA,'formB':formB,'words':words})

"""
class LecturesListView(ListView):

	model = Lecture
	paginate_by = 10  # if pagination is desired
	template_name = "dictionary/lectures_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
"""