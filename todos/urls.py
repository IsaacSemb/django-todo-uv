from django.urls import include, path
from . import views


# this avoid scoping issues if 2 apps have the same template name
app_name = 'todos'

urlpatterns = [
    path('', views.read_todos, name='todo_list_html'),
    path('add-todo/', views.create_todo, name='add_todo'),
    path('delete-todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('edit-todo/<int:todo_id>/', views.update_todo, name='edit_todo'),
]
