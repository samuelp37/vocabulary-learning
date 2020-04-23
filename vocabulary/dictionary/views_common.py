import sys

from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db import models as djangoModel

from .models import Word, Author
from .forms import WordForm, AuthorForm


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
    
# Generic class

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
        
class TranslationForeignKeyTranslationField():

    def __init__(self,model_name,model_form_name,field_autocomplete_name,user_based=False):
    
        self.field_autocomplete_name = field_autocomplete_name
        self.user_based = user_based
    
        self.autocomplete_fields = []
        self.autocomplete_fields.append(AutoCompletionNestedField(model_name=model_name,model_form_name=model_form_name,field_autocomplete_name=field_autocomplete_name,prefix="original_"+self.field_autocomplete_name,title="Original "+self.field_autocomplete_name,user_based=self.user_based))
        self.autocomplete_fields.append(AutoCompletionNestedField(model_name=model_name,model_form_name=model_form_name,field_autocomplete_name=field_autocomplete_name,prefix="translated_"+self.field_autocomplete_name,title="Translated "+self.field_autocomplete_name,user_based=self.user_based))
        
    def initialize_get(self,request,pre_instance=None):
    
        self.target_input_words = []
        self.forms = []
        print(pre_instance)
        for field in self.autocomplete_fields:
            form, target_input_id = field.autocomplete_form(request,pre_instance=pre_instance)
            self.forms.append(form)
            self.target_input_words.append(target_input_id)
        
        self.target_input_words = ",".join(self.target_input_words)
        
    def initialize_post(self,request):
    
        self.forms = []
        for field in self.autocomplete_fields:
            form, _ = field.autocomplete_form(request)
            self.forms.append(form)
        
        self.formA, self.formB = self.forms
        self.itemA, self.itemB = None, None
        
        if self.formA.is_valid() and self.formB.is_valid():
            self.itemA, boolA = self.autocomplete_fields[0].model.objects.get_or_create(**self.formA.cleaned_data)
            self.itemB, boolB = self.autocomplete_fields[1].model.objects.get_or_create(**self.formB.cleaned_data)
            return True
        else:
            print("Form A errors :")
            print(self.formA.errors)
            print(self.formA.non_field_errors())
            print("Form B errors :")
            print(self.formB.errors)
            print(self.formB.non_field_errors())
            
        return False
            
    def update_main_form(self,form):
   
        setattr(form, self.autocomplete_fields[0].prefix, self.itemA)
        setattr(form, self.autocomplete_fields[1].prefix, self.itemB)
        setattr(form, "slug", slugify(self.itemA.__str__() + "-" + self.itemB.__str__()))
        
    def update_variables_dict(self,variables_dict):
        new_dict = {}
        new_dict['formA_'+self.field_autocomplete_name] = self.forms[0]
        new_dict['formB_'+self.field_autocomplete_name] = self.forms[1]
        variables_dict['target_input_words'] += self.target_input_words
        variables_dict.update(new_dict)