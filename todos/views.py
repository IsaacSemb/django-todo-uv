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

    if request.method =='DELETE':
        print('delete requested')
        return redirect('todos:todo_list_html')
        

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


def create_todo(request):
    """
    This view on GET 
    it gets you the form to use  
    but on POST (coming from the form its self)  
    it processes the form data and saves it to the database
    """

    # possible origin is the add todo form
    if request.method == 'POST':

        # there is zero validation here, we shall get to that later
        Todo.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            user_id = request.user.id,
            status = request.POST['status'],
        )

        return redirect('todos:todo_list_html')

    todo_status = Todo.STATUS_CHOICES

    return render(request, "todos/add_todo.html", {'todo_status':todo_status})



def read_todo(request):
    pass

def read_todos(request):
    pass

def delete_todo(request):
    
    
    return redirect('todos:todo_list_html')


def delete_todos(request):
    return redirect('todos:todo_list_html')
