from django.db import models
import datetime
from django.contrib.auth.models import User

class QuizzLinkItem(models.Model):

    quizz = models.ForeignKey('Quizz',on_delete=models.CASCADE,default='')
    quizz_item = models.ForeignKey('QuizzItem',on_delete=models.CASCADE,default='')
	
    def __str__(self):
        return self.quizz.__str__()+"-"+self.quizz_item.__str__()
		
    class Meta:
        verbose_name = "Quizz - Item"
        verbose_name_plural = "Quizz - Items"
    
class QuizzItem(models.Model):

    translation = models.ForeignKey('Translation',on_delete=models.CASCADE,default='')
    original_to_translate = models.BooleanField(default=False)
    delivered_on = models.DateTimeField("Date of delivery",default=datetime.datetime.now(),null=True,blank=True)
    delta_reply = models.FloatField("Duration reply (s)",default=-1,null=True,blank=True)
    slug = models.SlugField("Slug",max_length=100,default='')
    success = models.BooleanField(default=False,null=True,blank=True)
    
    def __str__(self):
        return "Quizz : " + self.translation.__str__()
        
    @property
    def get_duration_s(self):
        if self.success:
            return "("+str(round(self.delta_reply,2))+"s)"
        else:
            return ""
        
    @property
    def get_class_itemlist(self):
        if self.success is None:
            return ""
        elif self.success:
            return "list-group-item-success"
        else:
            return "list-group-item-danger"
        
    class Meta:
        verbose_name = "Quizz item"
        verbose_name_plural = "Quizz items"

class Quizz(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    items = models.ManyToManyField('QuizzItem', through='QuizzLinkItem')
    date_quizz = models.DateField("Date of the quizz",default=datetime.date.today)
    slug = models.SlugField("Slug",max_length=100,default='')
    
    def __str__(self):
        return "Quizz ("+self.date_quizz.strftime("%d/%m/%Y")+")"
        
    @property
    def get_date(self):
        return self.date_quizz.strftime("%d/%m/%Y")
        
    @property
    def disabled_resume(self):
        count = self.items.all().filter(success=None).count()
        if count > 0:
            return ""
        else:
            return "disabled"
            
    @property
    def count_questions_quizz(self):
        count = self.items.all().exclude(success=None).count()
        return count
        
    @property
    def count_success_questions_quizz(self):
        count = self.items.all().filter(success=True).count()
        return count
        
    @property
    def get_ratio_success(self):
        return str(self.count_success_questions_quizz)+"/"+str(self.count_questions_quizz)
    
    @property
    def get_ratio_success_asint_percentage(self):
        return int(100*self.count_success_questions_quizz/self.count_questions_quizz)
		
    class Meta:
        verbose_name = "Quizz"
        verbose_name_plural = "Quizz"

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
    
    @property
    def nb_translations(self):
        return self.translations.all().count()
    
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
    translations = models.ManyToManyField('Translation', through='TranslationLink')
    
    def __str__(self):
        return self.title + "("+self.author.__str__()+")"
        
    @staticmethod
    def extern_slug():
        return "slug_book"
       
    @staticmethod
    def translation_utils():
        dict = {}
        dict["model_link"] = TranslationLink()
        dict["model_link_attr"] = "book"
        return dict
    
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
        
class Topic(models.Model):

    name = models.CharField("Name",max_length=100,default='',null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        
class Article(Support):

    topic = models.ForeignKey('Topic',on_delete=models.CASCADE,default='')
    newspaper = models.ForeignKey('Newspaper',on_delete=models.CASCADE,default='')
    link = models.TextField("Link to the article",default='',null=True,blank=True)
    translations = models.ManyToManyField('Translation', through='TranslationLinkArticle')
    
    def __str__(self):
        return self.title + "("+self.newspaper.name+")"
        
    @staticmethod    
    def extern_slug():
        return "slug_article"
        
    @staticmethod
    def translation_utils():
        dict = {}
        dict["model_link"] = TranslationLinkArticle()
        dict["model_link_attr"] = "article"
        return dict
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        
class Discussion(Support):

    topic = models.ForeignKey('Topic',on_delete=models.CASCADE,default='')
    translations = models.ManyToManyField('Translation', through='TranslationLinkDiscussion')
    
    original_content = models.TextField("Original content",default='',null=True,blank=True)
    translated_content = models.TextField("Original content",default='',null=True,blank=True)
    
    def __str__(self):
        return self.title + " ("+self.topic.name+")"
    
    @staticmethod
    def extern_slug():
        return "slug_discussion"
    
    @staticmethod
    def translation_utils():
        dict = {}
        dict["model_link"] = TranslationLinkDiscussion()
        dict["model_link_attr"] = "discussion"
        return dict
    
    class Meta:
        verbose_name = "Discussion"
        verbose_name_plural = "Discussions"

class Gender(models.Model):

    short = models.CharField("Short Gender",max_length=1,default='',null=True,blank=True)
    gender = models.CharField("Gender",max_length=20,default='',null=True,blank=True)
    
    def __str__(self):
        return self.gender
        
    def get_article(self, language):
        if language=="German":
            if self.gender=="Masculine":
                return "der "
            elif self.gender=="Feminine":
                return "die "
            elif self.gender=="Neutral":
                return "das "
        elif language=="French":
            if self.gender=="Masculine":
                return "un "
            elif self.gender=="Feminine":
                return "une "
        return ""
      
    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Genders"
        
class Word(models.Model):

    word = models.CharField("Word",max_length=100,default='',blank=False)
    plural = models.CharField("Plural",max_length=100,default='',blank=True)
    gender = models.ForeignKey('Gender',on_delete=models.CASCADE,default='')
    language = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
    
    def __str__(self):
        return self.gender.get_article(self.language.name) + self.word + " ("+self.language.name+")"
     
    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"
        
class Adjective(models.Model):

    word = models.CharField("Word",max_length=100,default='',blank=False)
    plural = models.CharField("Plural",max_length=100,default='',blank=True)
    language = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
    
    def __str__(self):
        return self.word + " ("+self.language.name+")"
     
    class Meta:
        verbose_name = "Adjective"
        verbose_name_plural = "Adjectives"
        
class Verb(models.Model):

    word = models.CharField("Word",max_length=100,default='',blank=False)
    language = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
    
    def __str__(self):
        return self.word + " ("+self.language.name+")"
     
    class Meta:
        verbose_name = "Verb"
        verbose_name_plural = "Verbs"
        
class Expression(models.Model):

    expression = models.TextField("Expression",default='',blank=False)
    language = models.ForeignKey('Language',on_delete=models.CASCADE,default='')
    
    def __str__(self):
        return self.expression + " ("+self.language.name+")"
     
    class Meta:
        verbose_name = "Expression"
        verbose_name_plural = "Expressions"
    
class Translation(models.Model):
    
    original_word = models.ForeignKey('Word',on_delete=models.CASCADE,default='',verbose_name="Original name",related_name="original_word",null=True,blank=True)
    translated_word = models.ForeignKey('Word',on_delete=models.CASCADE,default='',verbose_name="Translated name",related_name="translated_word",null=True,blank=True)
    
    original_adj = models.ForeignKey('Adjective',on_delete=models.CASCADE,default='',verbose_name="Original adjective",related_name="original_adj",null=True,blank=True)
    translated_adj = models.ForeignKey('Adjective',on_delete=models.CASCADE,default='',verbose_name="Translated adjective",related_name="translated_adj",null=True,blank=True)
    
    original_verb = models.ForeignKey('Verb',on_delete=models.CASCADE,default='',verbose_name="Original verb",related_name="original_verb",null=True,blank=True)
    translated_verb = models.ForeignKey('Verb',on_delete=models.CASCADE,default='',verbose_name="Translated verb",related_name="translated_verb",null=True,blank=True)
    
    original_exp = models.ForeignKey('Expression',on_delete=models.CASCADE,default='',verbose_name="Original expression",related_name="original_exp",null=True,blank=True)
    translated_exp = models.ForeignKey('Expression',on_delete=models.CASCADE,default='',verbose_name="Translated expression",related_name="translated_exp",null=True,blank=True)
    
    date_added = models.DateField("Date of edition",default=datetime.date.today)
    
    context_sentence = models.TextField("Context original sentence",default='',null=True,blank=True)
    translation_context_sentence = models.TextField("Translation of the context sentence",default='',null=True,blank=True)
    
    slug = models.SlugField("Slug",max_length=100,default='',null=True,blank=True)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    @property
    def original_str(self):
        if self.original_word:
            return self.original_word
        elif self.original_adj:
            return self.original_adj
        elif self.original_verb:
            return self.original_verb
        elif self.original_exp:
            return self.original_exp
            
    @property
    def translated_str(self):
        if self.translated_word:
            return self.translated_word
        elif self.translated_adj:
            return self.translated_adj
        elif self.translated_verb:
            return self.translated_verb
        elif self.translated_exp:
            return self.translated_exp
            
    @staticmethod
    def get_model_access_list():
        return [Book,Article,Discussion]
    
    def __str__(self):
        return self.original_str.__str__() + "-" + self.translated_str.__str__()
    
    @property    
    def short_str(self):
        return self.__str__()[:30]
        
    @property
    def count_questions_quizz(self):
        count = QuizzItem.objects.all().filter(translation=self).exclude(success=None).count()
        return count
        
    @property
    def count_success_questions_quizz(self):
        count = QuizzItem.objects.all().filter(translation=self,success=True).count()
        return count
        
    @property
    def get_ratio_success(self):
        return str(self.count_success_questions_quizz)+"/"+str(self.count_questions_quizz)
        
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
        
class TranslationLinkArticle(models.Model):
	
    item = models.ForeignKey('Translation',on_delete=models.CASCADE,default='')
    article = models.ForeignKey('Article',on_delete=models.CASCADE,default='')
	
    def __str__(self):
        return self.article.__str__()+"-"+self.item.__str__()
		
    class Meta:
        verbose_name = "Translation - Article"
        verbose_name_plural = "Translations - Articles"
        
class TranslationLinkDiscussion(models.Model):
	
    item = models.ForeignKey('Translation',on_delete=models.CASCADE,default='')
    discussion = models.ForeignKey('Discussion',on_delete=models.CASCADE,default='')
	
    def __str__(self):
        return self.discussion.__str__()+"-"+self.item.__str__()
		
    class Meta:
        verbose_name = "Translation - Discussion"
        verbose_name_plural = "Translations - Discussions"
    
        
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