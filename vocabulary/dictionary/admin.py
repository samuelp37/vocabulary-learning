from django.contrib import admin
from . import models

admin.site.register(models.Author)
admin.site.register(models.Language)
admin.site.register(models.Book)

class VocabularyItemAdmin(admin.ModelAdmin):
	search_fields = ('original_word',)
	list_filter = ('date_added',)

admin.site.register(models.Vocabulary,VocabularyItemAdmin)


admin.site.register(models.Lecture)
