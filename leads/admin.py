from django.contrib import admin

from .models import User, Lead, Agent, UserProfile, Category, FollowUp

class LeadAdmin(admin.ModelAdmin):
    # fields = (
    #     'first_name',
    #     'last_name',
    # )

    list_display = ['first_name', 'last_name', 'age', 'email']
    list_display_links = ['first_name']
    list_editable = ['last_name']
    list_filter = ['category']
    search_fields = ['first_name', 'last_name', 'email']


admin.site.register(User) #this is the admin page for the user model in the admin page of the website  
admin.site.register(Category) #this is the admin page for the category model in the admin page of the website
admin.site.register(UserProfile) #this is the admin page for the userprofile model in the admin page of the website
admin.site.register(Lead) #this is the admin page for the lead model in the admin page of the website
admin.site.register(Agent) #this is the admin page for the agent model in the admin page of the website
admin.site.register(FollowUp) #this is the admin page for the follow up model in the admin page of the website