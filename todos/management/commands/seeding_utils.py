"""
Shared seeding utilities that can be used by:
- Management commands
- Standalone scripts
- Other parts of the application

This avoids code duplication across different seeding methods.
"""

from django.contrib.auth.models import User
from todos.models import Todo


def seed_users_from_data(users_data, output_callback=None):
    """
    Seed users from JSON data.
    
    Args:
        users_data: List of user dictionaries
        output_callback: Optional function to call for output (e.g., stdout.write)
    
    Returns:
        tuple: (success_count, error_count)
    """
    success_count = 0
    error_count = 0
    
    for user_data in users_data:
        try:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
            )
            success_count += 1
            if output_callback:
                output_callback('success', f'✓ Created user: {user.username}')
            else:
                print(f"✓ Created user: {user.username}")
        except Exception as e:
            error_count += 1
            if output_callback:
                output_callback('error', f'✗ Error creating user {user_data["username"]}: {e}')
            else:
                print(f"✗ Error creating user {user_data['username']}: {e}")
    
    return success_count, error_count


def seed_todos_from_data(todos_data, output_callback=None):
    """
    Seed todos from JSON data.
    
    Args:
        todos_data: Dictionary with 'todos' key containing user groups
        output_callback: Optional function to call for output
    
    Returns:
        tuple: (success_count, error_count)
    """
    success_count = 0
    error_count = 0
    
    for user_group in todos_data['todos']:
        try:
            user = User.objects.get(username=user_group['username'])
            
            for todo_data in user_group['todos']:
                try:
                    todo = Todo.objects.create(
                        title=todo_data['title'],
                        description=todo_data['description'],
                        status=todo_data['status'],
                        user=user
                    )
                    success_count += 1
                    if output_callback:
                        output_callback('success', f'✓ Created todo: {todo.title} for {user.username}')
                    else:
                        print(f"✓ Created todo: {todo.title} for {user.username}")
                except Exception as e:
                    error_count += 1
                    if output_callback:
                        output_callback('error', f'✗ Error creating todo: {e}')
                    else:
                        print(f"✗ Error creating todo: {e}")
        except User.DoesNotExist:
            error_count += 1
            if output_callback:
                output_callback('error', f'✗ User {user_group["username"]} not found')
            else:
                print(f"✗ User {user_group['username']} not found")
    
    return success_count, error_count

