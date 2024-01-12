from django.urls import path #this is the path function from django.urls module (django/urls/__init__.py)
from .views import ( #this is the views.py file in the leads app folder (crm-django/leads/views.py)
    lead_list, lead_detail,lead_create,lead_update,lead_delete,
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView,
    AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView
)

app_name = "leads" #this is the app name for the leads app (crm-django/leads/apps.py)

urlpatterns = [
    path('', LeadListView.as_view(), name="lead-list"), #this is the path for the lead list page (crm-django/leads/templates/leads/lead_list.html)
    path('<int:pk>/', LeadDetailView.as_view(), name="lead-detail"), #this is the path for the lead detail page (crm-django/leads/templates/leads/lead_detail.html)
    path('<int:pk>/update/', LeadUpdateView.as_view(), name="lead-update"), #this is the path for the lead update page (crm-django/leads/templates/leads/lead_update.html)
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'), #this is the path for the lead delete page (crm-django/leads/templates/leads/lead_delete.html) 
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name="assign-agent"), #this is the path for the assign agent page (crm-django/leads/templates/leads/assign_agent.html)
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name="lead-category-update"), #this is the path for the lead category update page (crm-django/leads/templates/leads/lead_category_update.html)
    path('create/', LeadCreateView.as_view(), name="lead-create"), #this is the path for the lead create page (crm-django/leads/templates/leads/lead_create.html)
    path('categories/', CategoryListView.as_view(), name="category-list"), #this is the path for the category list page (crm-django/leads/templates/leads/category_list.html)
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name="category-detail"), #this is the path for the category detail page (crm-django/leads/templates/leads/category_detail.html)
]