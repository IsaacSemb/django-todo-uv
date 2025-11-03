from django.urls import include, path
from . import views


# this avoid scoping issues if 2 apps have the same template name
app_name = 'website'

urlpatterns = [
    path("", view=views.index, name="home"),
    path("about", view=views.about, name="about"),
    path("contact", view=views.contact, name="contact"),
    path("login", view=views.login_page, name="login"),
    path("signup", view=views.signup_page, name="signup"),
]
