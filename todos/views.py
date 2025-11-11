from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Todo

# Create your views here.
def todo_list_json(request):

    # get the user
    user = request.user
    print(user)
    if not user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)



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

    # check for the user
    user = request.user

    if not user or not user.is_authenticated:
        return redirect('website:login')
        
    # get the todos for the user
    todos = Todo.objects.filter(user=user)

    data = [
        {
            'id':todo.id,
            'title':todo.title,
            'description':todo.description,
            'status':todo.status,
        } for todo in todos
    ]

    return render(request, 'todos/todos.html', {'todos': data})
