from django.shortcuts import redirect, render, get_object_or_404
from .models import Todo
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

"""
THE LOGIN REQUIRED HELPS CUT OUT THE REPEATED CODE
LIKE THE ONE BELOW:

user = request.user
if not user or not user.is_authenticated:
    return redirect('website:login')
"""


@login_required
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
    if request.method == "POST":

        # there is zero validation here, we shall get to that later
        Todo.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            user_id=request.user.id,
            status=request.POST["status"],
        )

        return redirect("todos:todo_list_html")

    # GET: Pass None for todo to indicate add mode
    return render(
        request, "todos/add_todo.html", {"todo_status": todo_status, "todo": None}
    )


@login_required
def read_todos(request):
    """
    This view reads the todos for the user in context (the logged in user)
    """
    # get the todos for the user
    todos = Todo.objects.filter(user=request.user)

    # create a list of todos with the id, title, description, and status
    data = [
        {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "status": todo.get_status_display(),
        }
        for todo in todos
    ]

    return render(request, "todos/todos.html", {"todos": data})


@login_required
def update_todo(request, todo_id):
    """
    Edit view: GET shows form with existing todo data,
    POST updates the todo in database

    Security: Only allows users to update their own todos.
    Returns 404 if todo doesn't exist or doesn't belong to the user.
    """
    todo_status = Todo.STATUS_CHOICES

    # Get the todo and verify ownership - returns 404 if not found or not owned
    # This prevents users from accessing/modifying other users' todos
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if request.method == "GET":
        # Fetch the todo to edit (already retrieved above with ownership check)
        return render(
            request,
            "todos/add_todo.html",
            {
                "todo_status": todo_status,
                "todo": todo,  # Pass todo object to populate form
            },
        )

    # POST: Update the existing todo (ownership already verified above)
    if request.method == "POST":
        # Update using the todo object we already retrieved (ensures ownership)
        todo.title = request.POST["title"]
        todo.description = request.POST["description"]
        todo.status = request.POST["status"]
        todo.save()
        return redirect("todos:todo_list_html")

    return redirect("todos:todo_list_html")


@login_required
def delete_todo(request, todo_id):
    """
    This view deletes a todo for the user.

    Security: Only allows users to delete their own todos.
    Returns 404 if todo doesn't exist or doesn't belong to the user.
    """
    # Get the todo and verify ownership - returns 404 if not found or not owned
    # This prevents users from deleting other users' todos
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect("todos:todo_list_html")


@login_required
def delete_todos(request):
    """
    This view deletes all todos for the user
    """
    Todo.objects.filter(user=request.user).delete()
    return redirect("todos:todo_list_html")
