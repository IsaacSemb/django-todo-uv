from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'website/home.html')
    
def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST)
        print(list(request.POST))

        # authenticate here
        user = authenticate(request, username=username, password=password)
        print(user)

        if user:
            login(request, user)
            return redirect('todos:todo_list_html')
        else:
            return render(request, 'website/login.html', {'error':'Invalid Credentials, Try Again!'})
    
    return render(request, 'website/login.html')


def signup_page(request):
    return render(request, 'website/signup.html')


def logout_user(request):
    
    data = logout(request)
    print(data)	

    return redirect('website:home')









