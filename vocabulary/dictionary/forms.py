from . import models
from django.forms import ModelForm, Textarea

class VocForm(ModelForm):
	class Meta:
		model = models.Vocabulary
		exclude = ['date_added']
		widgets = {
			'context_sentence': Textarea(attrs={'cols': 80, 'rows': 2}),
			'translation_context_sentence': Textarea(attrs={'cols': 80, 'rows': 2})
        }