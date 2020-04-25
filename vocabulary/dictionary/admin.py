from django.contrib import admin
from . import models

admin.site.register(models.Author)
admin.site.register(models.Language)

admin.site.register(models.Newspaper)
admin.site.register(models.Article)
admin.site.register(models.Gender)
admin.site.register(models.Word)
admin.site.register(models.Adjective)
admin.site.register(models.Translation)
admin.site.register(models.TranslationLink)

class BookInline(admin.TabularInline):
	model = models.TranslationLink
	extra = 0

class BookAdmin(admin.ModelAdmin):

	inlines = [BookInline]
    
admin.site.register(models.Book,BookAdmin)

"""
class VocabularyItemAdmin(admin.ModelAdmin):
	search_fields = ('original_word',)
	list_filter = ('date_added',)

admin.site.register(models.Vocabulary,VocabularyItemAdmin)
"""