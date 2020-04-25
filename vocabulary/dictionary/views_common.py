import sys
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db import models as djangoModel
from django.views.generic.base import View
from django.urls import reverse

from .models import Word, Author, Adjective, Verb, Expression
from .forms import WordForm, AuthorForm, AdjectiveForm, VerbForm, ExpressionForm


# Utilities

def random_str(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
    
def get_all_fields_from_form(instance):
    """"
    Return names of all available fields from given Form instance.

    :arg instance: Form instance
    :returns list of field names
    :rtype: list
    """

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields
    
# Auto-completion view

class AutoCompletionView(View):

    def __init__(self,model,model_form,main_slug_name,slugs_list,template_path,nested_fields):
        self.model = model
        self.model_form = model_form
        self.main_slug_name = main_slug_name
        self.slugs_list = slugs_list
        self.template_path = template_path
        self.nested_fields = nested_fields
        
    def set_slug_user(self, request):
        self.item.user = self.item.user
        self.item.slug = slugify(self.item.title)
        
    def redirect_success(self,request,**kwargs):
        return HttpResponseRedirect(reverse('list_book'))
        
    def redirect_fail(self,request,**kwargs):
        return self.get(request)
        
    def post_save(self,update,**kwargs):
        pass
        
    def clean_useless_records(self):
        pass
        
    def custom_nested_fields_handler(self,request):
        success = True
        for field in self.nested_fields:
            success = field.initialize_post(request)
            if not success:
                return False
        return success
        
    def get(self, request, **kwargs):
        
        # Getting pre-instance
        pre_instance = self.model.objects.filter(slug=kwargs.get(self.main_slug_name)).first()
        
        # Creating a new form
        if pre_instance is None:
            form = self.model_form()
        else:
            form = self.model_form(instance=pre_instance)
            
        variables_dict = {'form':form,self.main_slug_name:kwargs.get(self.main_slug_name)}
          
        for slug in self.slugs_list:
            variables_dict[slug] = kwargs.get(slug)
          
        target_input_words = []
        #creating nested autocomplete forms
        for field in self.nested_fields:
            form, target_input_id = field.autocomplete_form(request,pre_instance)
            target_input_words.append(target_input_id)
            variables_dict["form_"+field.prefix] = form
        
        target_input_words = ",".join(target_input_words)
        variables_dict['target_input_words'] = target_input_words
        
        return render(request, self.template_path, variables_dict)
        
    def post(self, request, **kwargs):
    
        # Initialize main form
        pre_instance = self.model.objects.filter(slug=kwargs.get(self.main_slug_name)).first()
        
        if pre_instance is None:
            form = self.model_form(request.POST)
            update = False
        else:
            form = self.model_form(request.POST,instance=pre_instance)
            update = True
        
        success = self.custom_nested_fields_handler(request)
        
        if success:
            
            if form.is_valid():
                self.item = form.save(commit=False)
                for field in self.nested_fields:
                    field.update_main_form(self.item)
                self.set_slug_user(request)
                self.item.save()
                
                redirection = self.post_save(update,**kwargs)
                self.clean_useless_records()
                if redirection is not None:
                    return redirection
                
                return self.redirect_success(request,**kwargs)
        
        return self.redirect_fail(request,**kwargs)

    
# Auto-completion fields class

class AutoCompletionNestedField():

    def __init__(self,model_name,model_form_name,field_autocomplete_name,prefix,title,user_based):
        self.model_name = model_name
        self.model_form_name = model_form_name
        self.model = str_to_class(self.model_name)
        self.model_form = str_to_class(self.model_form_name)
        self.field_autocomplete_name = field_autocomplete_name
        self.prefix = prefix
        self.title = title
        self.user_based = user_based
        
    def get(self,request):
        return self.autocomplete_api(request)

    def autocomplete_api(self,request,max_number_suggestions=3):
           
        if request.is_ajax():
        
            kwargs = {
                '{0}__{1}'.format(self.field_autocomplete_name, 'startswith'): request.GET.get('search', None)
            }
            if not self.user_based:
                queryset = self.model.objects.filter(**kwargs)
            else:
                queryset = self.model.objects.filter(**kwargs).filter(user=request.user)
            
            list = []        
            for word in queryset[:max_number_suggestions]:
                dict_instance = []
                for field_name in get_all_fields_from_form(self.model_form):
                    attr = getattr(word, field_name)
                    if isinstance(attr,djangoModel.Model):
                        dict_instance.append(attr.id)
                    else:
                        dict_instance.append(attr)
                dict_instance.append(word.__str__())
                list.append(dict_instance)
            data = {
                'list': list,
            }

        return JsonResponse(data)
            
    def autocomplete_form(self,request,pre_instance=None):
        
        if request.method == 'POST':
            form = self.model_form(request.POST,prefix=self.prefix)
        else:
            if pre_instance is None:
                form = self.model_form(None,prefix=self.prefix)
            else:
                form = self.model_form(prefix=self.prefix, instance=getattr(pre_instance,self.prefix))
        
        target_input_id = "#id_"+form.prefix+"-"+self.field_autocomplete_name
        form.title = self.title
        form.list_fields = get_all_fields_from_form(self.model_form)
                
        return form, target_input_id
        
    def initialize_post(self,request):
    
        self.form, _ = self.autocomplete_form(request)
        self.item = None
        
        if self.form.is_valid():
            self.item, bool = self.model.objects.get_or_create(**self.form.cleaned_data)
            return True
        else:
            self.item = None
            print("Form errors :")
            print(self.form.errors)
            print(self.form.non_field_errors())
            
        return False
        
    def update_main_form(self,form):
   
        setattr(form, self.prefix, self.item)
