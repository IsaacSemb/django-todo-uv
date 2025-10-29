from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'website/home.html', {})

def about(request):
    return render(request, 'website/about.html', {})

def contact(request):
    return render(request, 'website/contact.html', {})
