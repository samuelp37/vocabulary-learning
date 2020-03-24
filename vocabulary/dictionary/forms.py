from dictionary.models import Translation, Word
from django.forms import ModelForm, Textarea

class TranslationForm(ModelForm):

    class Meta:
    
        model = Translation
        fields = '__all__'
        widgets = {
            'context_sentence': Textarea(attrs={'cols': 80, 'rows': 2}),
            'translation_context_sentence': Textarea(attrs={'cols': 80, 'rows': 2})
        }

    
class WordForm(ModelForm):

    class Meta:
    
        model = Word
        fields = '__all__'
