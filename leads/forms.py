from django import forms
from .models import Lead, Agent
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