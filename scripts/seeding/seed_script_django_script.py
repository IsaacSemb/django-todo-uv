

"""
MENTAL MODEL FOR HOW THINGS RUN

STEP 1: show python interpreter the path to the project root
    - We need to set the project root so that Python can locate and import modules from the project root
    - This is necessary so Python can locate and import modules from the project root,
    - especially when running this script directly from a subdirectory.

STEP 2: set the Django settings module and initialize Django
    - We need to set the Django settings module so that Django can find the settings.py file
    - This is necessary so Django can find the settings.py file
    - Also due to the fact that we are running this script directly from a subdirectory

STEP 3: import necessary Django related stuff 
    - We need to import necessary Django related stuff so that we can use Django functions
    - for our case we need the models that we shall interact with
    - basically from here you can use django normal syntax and functions
    - like making queries to the database, creating new objects, etc.
    - everything else will work as expected (i think or i hope LOL)

"""


import sys
from pathlib import Path
import os
import django
import json


# STEP 1: show python interpreter the path to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# STEP 2: set the Django settings module and initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_todo_fullstack.settings')
django.setup()

# STEP 3: from here we can use django normal syntax and functions

from django.contrib.auth.models import User
from todos.models import Todo

def seed_users(users_data):
    """Create users using Django ORM"""
    for user_data in users_data:
        try:
            # Django's create_user() handles password hashing automatically!
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],  # Automatically hashed!
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
            )
            print(f"✓ Created user: {user.username}")
        except Exception as e:
            print(f"✗ Error creating user {user_data['username']}: {e}")


def seed_todos(todos_data):
    """Create todos using Django ORM"""
    for user_group in todos_data['todos']:
        # Get user by username (or user_id)
        try:
            user = User.objects.get(username=user_group['username'])
            
            for todo_data in user_group['todos']:
                try:
                    todo = Todo.objects.create(
                        title=todo_data['title'],
                        description=todo_data['description'],
                        status=todo_data['status'],
                        user=user  # Django handles the foreign key!
                    )
                    print(f"✓ Created todo: {todo.title} for {user.username}")
                except Exception as e:
                    print(f"✗ Error creating todo: {e}")
        except User.DoesNotExist:
            print(f"✗ User {user_group['username']} not found")

def main():
    """Main seeding function"""
    script_dir = Path(__file__).parent
    users_file = script_dir / 'mock_data' / 'users.json'
    todos_file = script_dir / 'mock_data' / 'todos.json'
    
    with open(users_file, 'r') as f:
        users_data = json.load(f)
    
    with open(todos_file, 'r') as f:
        todos_data = json.load(f)
    
    print("\n=== Seeding Users (Django ORM) ===")
    seed_users(users_data)
    
    print("\n=== Seeding Todos (Django ORM) ===")
    seed_todos(todos_data)
    
    print("\n✓ Seeding complete!")

if __name__ == "__main__":
    main()