from dictionary.models import Translation, Word, Book, Author
from django.forms import ModelForm, Textarea, DateInput
from django.contrib.admin import widgets 

class TranslationForm(ModelForm):

    class Meta:
    
        model = Translation
        fields = ['date_added']
        widgets = {
            'context_sentence': Textarea(attrs={'cols': 80, 'rows': 2}),
            'translation_context_sentence': Textarea(attrs={'cols': 80, 'rows': 2}),
            'date_added': DateInput(format='%Y-%m-%d',attrs={'class':'my-datepicker'}),
        }

class WordForm(ModelForm):

    class Meta:
    
        model = Word
        fields = "__all__"
        """
        widgets = {
            'context_sentence': Textarea(attrs={'cols': 80, 'rows': 2}),
        }
        """
        
    """
    class Media:
        js = ('js/search_list_word.js',)
    """
    
class BookForm(ModelForm):

    class Meta:
    
        model = Book
        exclude = ['author','slug','translations','user']
        
class AuthorForm(ModelForm):

    class Meta:
    
        model = Author
        fields = '__all__'