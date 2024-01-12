from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()
class AgentModelForm(forms.ModelForm): #this is the agent model form that inherits from the model form class
    class Meta:
        model = User
        fields = ( #these are the fields for the agent model form
            'email',
            'username',
            'first_name',
            'last_name',
        )       
