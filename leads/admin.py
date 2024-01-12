from django.contrib import admin

from .models import User, Lead, Agent, UserProfile, Category

admin.site.register(User) #this is the admin page for the user model in the admin page of the website  
admin.site.register(Category) #this is the admin page for the category model in the admin page of the website
admin.site.register(UserProfile) #this is the admin page for the userprofile model in the admin page of the website
admin.site.register(Lead) #this is the admin page for the lead model in the admin page of the website
admin.site.register(Agent) #this is the admin page for the agent model in the admin page of the website
