from django.urls import include, path
from . import views

urlpatterns = [
    path("index", view=views.index, name="home"),
    path("about", view=views.about, name="about"),
    path("contact", view=views.contact, name="contact"),
]
