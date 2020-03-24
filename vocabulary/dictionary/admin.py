from django.contrib import admin
from . import models

admin.site.register(models.Author)
admin.site.register(models.Language)
admin.site.register(models.Book)
admin.site.register(models.Newspaper)
admin.site.register(models.Article)
admin.site.register(models.Gender)
admin.site.register(models.Word)
admin.site.register(models.Translation)
"""
class VocabularyItemAdmin(admin.ModelAdmin):
	search_fields = ('original_word',)
	list_filter = ('date_added',)

admin.site.register(models.Vocabulary,VocabularyItemAdmin)
"""