from django.shortcuts import render
from . import forms
from django.views.generic.list import ListView
from . import models
from django.http import HttpResponse
import random
import string

def home(request):
    return HttpResponse('Hello, World!')

class Entry:
    
    def __init__(self,word,article,lng):
        self.word = word
        self.article = article
        self.lng = lng
        
def random_str(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))

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
        
        target_words_input_id = "#id_"+formA.prefix+"-word,#id_"+formB.prefix+"-word"
        formA.title = "Original word"
        formB.title = "Translated word"
        
        #words = models.Word.objects.all()
        #words = {0:"word",1:"wordb"}
        words = {}
        for i in range(10000):
            words[i] = [random_str(10),random.choice([1,2,3,4]),random.choice([1,2,3])];
        #words = {0:["Schwierigkeit",2,2],1:["difficulty",4,1]}
        #print(words)
        
    #returning form 
    return render(request, 'dictionary/vocform.html', {'form':form,'formA':formA,'formB':formB,'words':words,'target_words_input_id':target_words_input_id})

"""
class LecturesListView(ListView):

	model = Lecture
	paginate_by = 10  # if pagination is desired
	template_name = "dictionary/lectures_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
"""