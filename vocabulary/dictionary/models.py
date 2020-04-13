from django.db import models
import datetime
from django.contrib.auth.models import User

class Author(models.Model):

    first_name = models.CharField("First name",max_length=100,default='',null=True,blank=True)
    last_name = models.CharField("Last name",max_length=100,default='',null=True,blank=True)
    
    def __str__(self):
        return self.first_name+" "+self.last_name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
 
class Language(models.Model):
    
    name = models.CharField("Name",max_length=100,default='',null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

class Support(models.Model):

    title = models.CharField("Title",max_length=100,default='')
    language = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
    slug = models.SlugField("Slug",max_length=100,default='',null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        unique_together = ("slug")
        verbose_name = "Support"
        verbose_name_plural = "Supports"
        
class Book(Support):

    author = models.ForeignKey('Author',on_delete=models.CASCADE,default='')
    subtitle = models.CharField("Subtitle",max_length=100,default='',null=True,blank=True)
    nb_pages = models.IntegerField("Number of pages",default=-1,null=True,blank=True)
    translations = models.ManyToManyField('Translation', through='TranslationLink',null=True,blank=True)
    
    def __str__(self):
        return self.title + "("+self.author.__str__()+")"
        
    @property
    def nb_translations(self):
        return self.translations.all().count()
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        
class Newspaper(models.Model):

    name = models.CharField("Name",max_length=100,default='',null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Newspaper"
        verbose_name_plural = "Newspapers"
        
class Article(Support):

    author = models.ForeignKey('Author',on_delete=models.CASCADE,default='')
    newspaper = models.ForeignKey('Newspaper',on_delete=models.CASCADE,default='')
    link = models.TextField("Link to the article",default='',null=True,blank=True)
    
    def __str__(self):
        return self.title + "("+self.newspaper+")"
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

class Gender(models.Model):

    short = models.CharField("Short Gender",max_length=1,default='',null=True,blank=True)
    gender = models.CharField("Gender",max_length=20,default='',null=True,blank=True)
    
    def __str__(self):
        return self.gender
        
    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Genders"
        
class Word(models.Model):

    word = models.CharField("Word",max_length=100,default='')
    gender = models.ForeignKey('Gender',on_delete=models.CASCADE,default='')
    language = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
    
    def __str__(self):
        return self.word + "("+self.language.name+")"
     
    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"
    
class Translation(models.Model):
    
    original_word = models.ForeignKey('Word',on_delete=models.CASCADE,default='',verbose_name="Original word",related_name="original_word")
    translated_word = models.ForeignKey('Word',on_delete=models.CASCADE,default='',verbose_name="Translated word",related_name="translated_word")
    
    date_added = models.DateField("Date of edition",default=datetime.date.today)
    
    context_sentence = models.TextField("Context original sentence",default='',null=True,blank=True)
    translation_context_sentence = models.TextField("Translation of the context sentence",default='',null=True,blank=True)
    
    slug = models.SlugField("Slug",max_length=100,default='',null=True,blank=True)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.original_word.word + " - "+self.translated_word.word
        
    class Meta:
        verbose_name = "Translation"
        verbose_name_plural = "Translations"
        
class TranslationLink(models.Model):
	
    item = models.ForeignKey('Translation',on_delete=models.CASCADE,default='')
    book = models.ForeignKey('Book',on_delete=models.CASCADE,default='')
	
    def __str__(self):
        return self.book.__str__()+"-"+self.item.__str__()
		
    class Meta:
        verbose_name = "Translation - Book"
        verbose_name_plural = "Translations - Books"
    
        
class Vocabulary(models.Model):

    original_word = models.CharField("Original word",max_length=100,default='')
    translation = models.CharField("Translation",max_length=100,default='')
    
    context_sentence = models.TextField("Context original sentence",default='',null=True,blank=True)
    translation_context_sentence = models.TextField("Translation of the context sentence",default='',null=True,blank=True)
    
    date_added = models.DateField("Date of edition",default=datetime.date.today)
    
    def __str__(self):
        return self.original_word + " ("+self.translation+")"
    
        verbose_name = "Vocabulary"
        verbose_name_plural = "Vocabularies"