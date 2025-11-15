from django.contrib import admin
from .models import Todo

admin.site.site_header = "Todo App Admin"
admin.site.site_title = "Todos Admin Portal"
admin.site.index_title = "Welcome to Todos Admin Portal"

# Register your models here.
admin.site.register(Todo)