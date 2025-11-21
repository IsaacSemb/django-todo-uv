from django.shortcuts import redirect, render
from .models import Todo


def create_todo(request):
    """
    This view on GET 
    it gets you the form to use  
    but on POST (coming from the form its self)  
    it processes the form data and saves it to the database
    """

    # get the status choices
    todo_status = Todo.STATUS_CHOICES

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

    # GET: Pass None for todo to indicate add mode
    return render(request, "todos/add_todo.html", {
        'todo_status': todo_status,
        'todo': None
    })

def read_todos(request):
    """
    This view reads the todos for the user in context (the logged in user)

    """

    # check for the user
    user = request.user

    # check if the user is authenticated, if not redirect to the login page
    if not user or not user.is_authenticated:
        return redirect('website:login')
        
    # get the todos for the user
    todos = Todo.objects.filter(user=user)

    # create a list of todos with the id, title, description, and status
    data = [
        {
            'id':todo.id,
            'title':todo.title,
            'description':todo.description,
            'status':todo.status,
        } for todo in todos
    ]

    return render(request, 'todos/todos.html', {'todos': data})


def update_todo(request, todo_id):
    """
    Edit view: GET shows form with existing todo data,
    POST updates the todo in database
    """
    todo_status = Todo.STATUS_CHOICES

    if request.method == 'GET':
        # Fetch the todo to edit
        todo = Todo.objects.get(id=todo_id)
        return render(request, "todos/add_todo.html", {
            'todo_status': todo_status,
            'todo': todo  # Pass todo object to populate form
        })
    
    # POST: Update the existing todo
    if request.method == 'POST':
        Todo.objects.filter(id=todo_id).update(
            title=request.POST['title'],
            description=request.POST['description'],
            status=request.POST['status'],
        )
        return redirect('todos:todo_list_html')

    return redirect('todos:todo_list_html')


def delete_todo(request, todo_id):
    """
    This view deletes a todo for the user
    """
    Todo.objects.filter(id=todo_id).delete()
    
    return redirect('todos:todo_list_html')


def delete_todos(request):
    """
    This view deletes all todos for the user
    """
    Todo.objects.filter(user=request.user).delete()
    return redirect('todos:todo_list_html')
