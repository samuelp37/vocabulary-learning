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
    
def addbookform(request):
    form = None
    #if form is submitted
    if request.method == 'POST':
    
        formA = forms.AuthorForm(request.POST,prefix="author")
        form = forms.BookForm(request.POST)
        
        # Adding the 2 words
        if formA.is_valid():
            authorA, boolA = models.Author.objects.get_or_create(**formA.cleaned_data)
            
            if form.is_valid():
                book = form.save(commit=False)
                book.author = authorA
                book.save()
            else:
                print(form.cleaned_data)
                print(form.non_field_errors())
                print([ (field.label, field.errors) for field in form])
        else:
            print(formA.cleaned_data)
            print(formA.non_field_errors())
            print([ (field.label, field.errors) for field in formA])
   
    #creating a new form
    form = forms.BookForm()
    formA = forms.AuthorForm(prefix="author")
    
    target_words_input_id = "#id_"+formA.prefix+"-first_name"
    formA.title = "Author"
    
    authors_queryset = models.Author.objects.all()
    
    authors = {}
    for i in range(len(authors_queryset)):
        author_tmp = authors_queryset[i]
        authors[i] = [author_tmp.first_name,author_tmp.last_name]
        
    #returning form 
    return render(request, 'dictionary/bookform.html', {'form':form,'formA':formA,'authors':authors,'target_words_input_id':target_words_input_id})


def translationform(request):
    form = None
    #if form is submitted
    if request.method == 'POST':
    
        formA = forms.WordForm(request.POST,prefix="original")
        formB = forms.WordForm(request.POST,prefix="translate")
        form = forms.TranslationForm(request.POST)
        
        # Adding the 2 words
        if formA.is_valid() and formB.is_valid():
            wordA, boolA = models.Word.objects.get_or_create(**formA.cleaned_data)
            wordB, boolB = models.Word.objects.get_or_create(**formB.cleaned_data)
            form.original_word = wordA
            form.translated_word = wordB
            
            if form.is_valid():
                translate = form.save(commit=False)
                translate.original_word = wordA
                translate.translated_word = wordB
                translate.save()
            else:
                print(form.cleaned_data)
                print(form.non_field_errors())
                print([ (field.label, field.errors) for field in form])
        else:
            print(formA.cleaned_data)
            print(formA.non_field_errors())
            print([ (field.label, field.errors) for field in formA])
   
    #creating a new form
    form = forms.TranslationForm()
    formA = forms.WordForm(prefix="original")
    formB = forms.WordForm(prefix="translate")
    
    target_words_input_id = "#id_"+formA.prefix+"-word,#id_"+formB.prefix+"-word"
    formA.title = "Original word"
    formB.title = "Translated word"
    
    words_queryset = models.Word.objects.all()
    
    words = {}
    for i in range(len(words_queryset)):
        word_tmp = words_queryset[i]
        words[i] = [word_tmp.word,word_tmp.gender.id,word_tmp.language.id]
        
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