from django import forms
from .models import Lead, Agent, Category, FollowUp
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model() 
class LeadModelForm(forms.ModelForm):
    class Meta:
        model=Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )

def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        # if data != "Joe":
        #     raise ValidationError("Your name is not Joe")
        return data

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request") #this is the request object that is passed in the view
        agents = Agent.objects.filter() 
        super(AssignAgentForm, self).__init__(*args, **kwargs) 
        self.fields["agent"].queryset = agents 

class LeadCategoryUpdateForm(forms.ModelForm): #this is the form for the category field in the lead model
    class Meta: #this is the meta class for the LeadCategoryUpdateForm
        model = Lead
        fields = (
            'category', #this is the field for the category
        )

class CategoryModelForm(forms.ModelForm): #this is the form for the category model
    class Meta:
        model = Category
        fields = (
            'name',
        )

class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'file'
        )