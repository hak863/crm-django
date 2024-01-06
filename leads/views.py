from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    context = {
        "name": "Hakr",
        "age": 20
    }
    return render(request, "second_page.html",context)
