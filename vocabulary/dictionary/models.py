from django.db import models
import datetime

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

	author = models.ForeignKey('Author',on_delete=models.CASCADE,default='')
	language = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
	title = models.CharField("Title",max_length=100,default='',null=True,blank=True)
	
	def __str__(self):
		return self.title+" ("+self.author.__str__()+")"

	class Meta:
		verbose_name = "Support"
		verbose_name_plural = "Supports"
		
class Book(Support):

	subtitle = models.CharField("Subtitle",max_length=100,default='',null=True,blank=True)
	nb_pages = models.IntegerField("Number of pages",default=-1,null=True,blank=True)
    
    @property
    def resource_name(self):
        return "Book"
	
	class Meta:
		verbose_name = "Book"
		verbose_name_plural = "Books"
		
class Lecture(models.Model):

	support = models.ForeignKey('Support',on_delete=models.CASCADE,default='')
	language_reference = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
	
	def __str__(self):
		return self.support.__str__()+" (Translation in "+self.language_reference.__str__()+")"
	
	class Meta:
		verbose_name = "Lecture"
		verbose_name_plural = "Lectures"
		
class Vocabulary(models.Model):

	original_word = models.CharField("Original word",max_length=100,default='',null=True,blank=True)
	translation = models.CharField("Translation",max_length=100,default='',null=True,blank=True)
	
	index_page = models.IntegerField("Index of the page/paragraph... (or other)",default=-1,null=True,blank=True)
	
	context_sentence = models.TextField("Context original sentence",default='',null=True,blank=True)
	translation_context_sentence = models.TextField("Translation of the context sentence",default='',null=True,blank=True)
	
	date_added = models.DateField("Date of edition",default=datetime.date.today)
	
	lecture_ref = models.ForeignKey('Lecture',on_delete=models.CASCADE,default='',verbose_name='Lecture',related_name='lecture_ref',null=True,blank=True)
	
	def __str__(self):
		return self.original_word + " ("+self.translation+")"
	
	class Meta:
		verbose_name = "Vocabulary"
		verbose_name_plural = "Vocabularies"