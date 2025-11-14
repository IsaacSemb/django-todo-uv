from django.urls import include, path
from . import views


# this avoid scoping issues if 2 apps have the same template name
app_name = 'todos'

urlpatterns = [
    path('', views.todo_list_html, name='todo_list_html'),
    path('list_json/', views.todo_list_json, name='todo_list_json'),
    path('add-todo/', views.create_todo, name='add_todo'),
    path('delete-todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('edit-todo/<int:todo_id>/', views.edit_todo, name='edit_todo'),
]
