from dictionary.models import Translation, Word, Book, Author, Adjective, Verb, Expression, Newspaper, Article, Topic, Discussion
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
        
class AdjectiveForm(ModelForm):

    class Meta:
    
        model = Adjective
        fields = "__all__"
        
class VerbForm(ModelForm):

    class Meta:
    
        model = Verb
        fields = "__all__"
        
class ExpressionForm(ModelForm):

    class Meta:
    
        model = Expression
        fields = "__all__"
    
class BookForm(ModelForm):

    class Meta:
    
        model = Book
        exclude = ['author','slug','translations','user']
        
class ArticleForm(ModelForm):

    class Meta:
    
        model = Article
        exclude = ['newspaper','slug','translations','user','topic']
        
class DiscussionForm(ModelForm):

    class Meta:
    
        model = Discussion
        exclude = ['slug','translations','user','topic']
        
class AuthorForm(ModelForm):

    class Meta:
    
        model = Author
        fields = '__all__'
        
class NewspaperForm(ModelForm):

    class Meta:
    
        model = Newspaper
        fields = '__all__'
        
class TopicForm(ModelForm):

    class Meta:
    
        model = Topic
        fields = '__all__'