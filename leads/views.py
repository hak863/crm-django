import logging
import datetime
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail
# from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganiserAndLoginRequiredMixin
from .models import Lead, Agent, Category, FollowUp
from .forms import (
    LeadForm, 
    LeadModelForm,  
    CustomUserCreationForm, 
    AssignAgentForm, 
    LeadCategoryUpdateForm,
    CategoryModelForm,
    FollowUpModelForm
)

# logger = logging.getLogger(__name__)

#CRUD + L  - Create, Retrieve, Update and Delete + List

class SignupView(generic.CreateView): #Class based view for the create view
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

def landing_page(request): #request is the request object
    return render(request, "landing.html")

class DashboardView(OrganiserAndLoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        # How many leads we have in total
        total_lead_count = Lead.objects.filter().count()

        # How many new leads in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = Lead.objects.filter(
            date_added__gte=thirty_days_ago
        ).count()

        # How many converted leads in the last 30 days
        converted_category = Category.objects.get(name="Converted")
        converted_in_past30 = Lead.objects.filter(
            category=converted_category,
            converted_date__gte=thirty_days_ago
        ).count()

        context.update({
            "total_lead_count": total_lead_count,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30
        })
        return context

class LeadListView(LoginRequiredMixin, generic.ListView): #Class based view for the List view
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads" #this is the name of the queryset in the template

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(agent__isnull=False)
        else:
            queryset = Lead.objects.filter(agent__isnull=False)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context= super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset,
            })
        return context
    

def lead_list(request):
    leads=Lead.objects.all() #queryset
    context = {
        "leads": leads 
    } #dictionary
    return render(request, "leads/lead_list.html",context) #rendering the template

class LeadDetailView(LoginRequiredMixin, generic.DetailView): #class based view for the detail view
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter()
        else:
            queryset = Lead.objects.filter()
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

def lead_detail(request, pk): #pk is primary key to identify the lead in the database and open the detailed view of the lead
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView): #Class based view for the create view
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list") #to dynamically get the lead list url
    
    def form_valid(self, form): #To send mail 
        if form.is_valid():
            lead = form.save(commit=False)
            lead.save()
            messages.success(self.request, "You have successfully created a lead")
            if lead.agent:  # Check if the lead is assigned to an agent
                send_mail(
                    subject="A lead has been created",
                    message="Go to the site to see the new lead",
                    from_email="admin@hkcrm.com",
                    recipient_list=[lead.agent.user.email]
                )
                
        return super(OrganiserAndLoginRequiredMixin, self).form_valid(form)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save() #this will save the form in the database
        return redirect("/leads")  
    context = {
        "form" : form
    }
    return render(request, "leads/lead_create.html",context)

class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView): #Class based view for the create view
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter()
    
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save() #this will save the form in the database
        return redirect("/leads")  
    context = {
        "form" : form,  
        "lead" : lead
    }
    return render(request, "leads/lead_update.html",context)

class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView): #Class based view for the delete view
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter()
    
def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete() #this will delete the lead from the database
    return redirect("/leads")


class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView): #Class based view for the assign agent view
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({ #this is to pass the request object to the form
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        send_mail( #to send mail to the agent who has been assigned the lead
                subject="A lead has been created",
                message="Go to the site to see the new lead",
                from_email="admin@hkcrm.com",
                recipient_list=[lead.agent.user.email]
                )
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView): #Class based view for the category list view
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context= super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter()
        else:
            queryset = Lead.objects.filter()
        context.update({
            "unassigned_lead_count": Lead.objects.filter(category__isnull=True).count(), #this is to get the count of the unassigned leads
        })
        return context

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter()
        else:
            queryset = Lead.objects.filter()
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView): #Class based view for the category detail view
    template_name = "leads/category_detail.html"
    context_object_name = "category"
  
    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter()
        else:
            queryset = Lead.objects.filter()
        return queryset

class CategoryCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView): #Class based view for the category create view
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)
    
class CategoryUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView): #Class based view for the category update view
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter()
        else:
            queryset = Category.objects.filter()
        return queryset

class CategoryDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView): #Class based view for the category delete view
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter()
        else:
            queryset = Category.objects.filter()
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView): #Class based view for the lead category update view
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})
    
    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter()
        else:
            queryset = Lead.objects.filter()
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

class FollowUpCreateView(LoginRequiredMixin, generic.CreateView): #Class based view for the follow up create view
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)

class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView): #Class based view for the follow up update view
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = FollowUp.objects.filter()
        else:
            queryset = FollowUp.objects.filter()
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().lead.id})

class FollowUpDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView): #Class based view for the follow up delete view
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = FollowUp.objects.filter()
        else:
            queryset = FollowUp.objects.filter()
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

""" def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm()
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            lead.first_name = first_name
            lead.last_name = last_name
            lead.age = age
            lead.save()
    context = {
        "form" : form
    }
    context = {
        "form" : form,  
        "lead" : lead
    }
    return render(request, "leads/lead_update.html",context) """

""" def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.first()
            if agent:
                Lead.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    agent=agent
                )
                return redirect("/leads")  
            else:
                print("No agent found")
    context = {
        "form" : form
    }
    return render(request, "leads/lead_create.html",context)  """  