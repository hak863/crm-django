from typing import Any
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from agents.mixins import OrganiserAndLoginRequiredMixin

#CRUD

class SignupView(generic.CreateView): #Class based view for the create view
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")



class LandingPageView(generic.TemplateView): #TemplateView is a class based view
    template_name = "landing.html"

def landing_page(request): #request is the request object
    return render(request, "landing.html")

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
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
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
        # TODO send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
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


class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
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
        lead= Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
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


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
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

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
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