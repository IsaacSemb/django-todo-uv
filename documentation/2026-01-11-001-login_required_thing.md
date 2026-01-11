
login required decorator:
    - it checks if the user is authenticated
    - if not, it redirects to the login page
    - if the user is authenticated, it allows the view to execute
    - it is a good practice to use it in all views that are related to the user
    - it is used to protect the views from unauthorized access

if unauthorised access is attempted, it will redirect to the login page
django was set to go to 
- accounts/login/
this is the default login page, that the devs chose a long time ago

but since django is set up to be unopionated, 
it allows the developer to change the login page to anything they want

by settings the LOGIN_URL in the settings.py file
even better, is to set the LOGIN_REDIRECT_URL in the settings.py file
the redirect is where the user will be redirected to after successful login

LOGIN_URL = 'website:login'
LOGIN_REDIRECT_URL = 'todos:todo_list_html'

this takes on both literal and url name meaning which is so cool
taking on url names means if anything in the url changes, the redirect will still work

here is how imagine it works
( and i know it does alot more than this but this is for my sanity)


```python

# the decorator somewhere in the django 
def login_required(view_function):
    def wrapper(request, *args, **kwargs):

        # this is what i wanted to emphasize, this is the repeated
        # functionality that we want so we dont have to sprinkle it everywhere
        if not request.user.is_authenticated:
            return redirect("/login") # or something like settings.LOGIN_URL 


        return view_function(request, *args, **kwargs)

    return wrapper

# usage 
@login_required
def create_todo(request):
    return HttpResponse("Todo created")

```