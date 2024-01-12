from django.urls import path
from .views import (
    AgentListView, AgentCreateView, 
    AgentDetailView, AgentUpdateView, 
    AgentDeleteView,
    )

app_name = "agents"

urlpatterns = [
    path('', AgentListView.as_view(), name="agent-list"), #this is the path for the agent list page (crm-django/agents/templates/agents/agent_list.html)
    path('create/', AgentCreateView.as_view(), name="agent-create"), #this is the path for the agent create page (crm-django/agents/templates/agents/agent_create.html)
    path('<int:pk>/', AgentDetailView.as_view(), name="agent-detail"), #this is the path for the agent detail page (crm-django/agents/templates/agents/agent_detail.html)
    path('<int:pk>/update/', AgentUpdateView.as_view(), name="agent-update"), #this is the path for the agent update page (crm-django/agents/templates/agents/agent_update.html)
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name="agent-delete"), #this is the path for the agent delete page (crm-django/agents/templates/agents/agent_delete.html)
]