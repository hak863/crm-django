from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm


class LandingPageView(TemplateView): #TemplateView is a class based view
    template_name = "landing.html"

def landing_page(request): #request is the request object
    return render(request, "landing.html")

class LeadListView(ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads" #this is the name of the queryset in the template

def lead_list(request):
    leads=Lead.objects.all() #queryset
    context = {
        "leads": leads 
    } #dictionary
    return render(request, "leads/lead_list.html",context) #rendering the template

def lead_detail(request, pk): #pk is primary key to identify the lead in the database and open the detailed view of the lead
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

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

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete() #this will delete the lead from the database
    return redirect("/leads")

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