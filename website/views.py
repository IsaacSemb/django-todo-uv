from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


# Create your views here.
def index(request):
    """
    This view renders the home page
    """
    return render(request, 'website/home.html')
    
def about(request):
    """
    This view renders the about page
    """
    return render(request, 'website/about.html')

def contact(request):
    """
    This view renders the contact page
    """
    return render(request, 'website/contact.html')

def login_page(request):
    """
    This view renders the login page
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate here
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('todos:todo_list_html')
        else:
            return render(request, 'website/login.html', {'error':'Invalid Credentials, Try Again!'})
    
    return render(request, 'website/login.html')


def signup_page(request):
    """
    This view renders the signup page
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')


        if User.objects.filter(username=username).exists():
            return render(request, 'website/signup.html', {'error':'Username already exists!'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'website/signup.html', {'error':'Email already exists!'})

        if password != password_confirm:
            return render(request, 'website/signup.html', {'error':'Passwords do not match!'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return redirect('todos:todo_list_html')

    return render(request, 'website/signup.html')


def logout_user(request):
    """
    This view logs out the user
    """
    logout(request)
    return redirect('website:home')