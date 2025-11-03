from django.shortcuts import render
from django.http import JsonResponse
from .models import Todo

# Create your views here.
def todo_list_json(request):
    todos = Todo.objects.all()
    data = [
        {
            "id": t.id, 
            "title": t.title,
            "description": t.description,
            "status": t.status
        } for t in todos
    ]
    return JsonResponse(data, safe=False)

def todo_list_html(request):
    
    todos = Todo.objects.all()

    data = [
        {
            'id':todo.id,
            'title':todo.title,
            'description':todo.description,
            'status':todo.status,
        } for todo in todos
    ]

    return render(request, 'todos/todos.html', {'todos': data})
