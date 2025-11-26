"""
MENTAL MODEL FOR HOW THINGS RUN USING DJANGO MANAGEMENT COMMANDS

Django management commands are a way to interact with Django applications from the command line.
django provided this functionality to make it easier to interact with the application from the command line.
we can draft CLI commands that can do all sorts of automated tasks like seeding the database, etc.


"""

from django.core.management.base import BaseCommand
import json
from pathlib import Path

# Import shared seeding utilities to avoid code duplication
from .seeding_utils import seed_users_from_data, seed_todos_from_data

class Command(BaseCommand):
    """
    Django management command class.
    The name 'Command' is required - Django looks for this class.
    """
    
    # this is what appears on typing in the command with the --help flag
    # manage.py <command> --help
    help = 'Seeds the database with users and todos from JSON files'


    def add_arguments(self, parser):
        """
        Add command-line arguments.
        This is optional - you can have commands without arguments.
        """
        parser.add_argument(
            '--users-file',
            type=str,
            default=None,
            help='Path to users JSON file (default: scripts/seeding/mock_data/users.json)'
        )
        parser.add_argument(
            '--todos-file',
            type=str,
            default=None,
            help='Path to todos JSON file (default: scripts/seeding/mock_data/todos.json)'
        )
    
    def handle(self, *args, **options):
        """
        This is the main method that runs when you execute the command.
        """
        # Get file paths from arguments or use defaults
        project_root = Path(__file__).parent.parent.parent.parent

        
        users_file = options.get('users_file') or project_root / 'scripts' / 'seeding' / 'mock_data' / 'users.json'
        todos_file = options.get('todos_file') or project_root / 'scripts' / 'seeding' / 'mock_data' / 'todos.json'
        
        # Load JSON data
        with open(users_file, 'r') as f:
            users_data = json.load(f)
        
        with open(todos_file, 'r') as f:
            todos_data = json.load(f)
        
        # Create output callback for styled output
        def output_callback(level, message):
            if level == 'success':
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))
        
        # Seed users using shared utility
        self.stdout.write(self.style.SUCCESS('\n=== Seeding Users ==='))
        user_success, user_errors = seed_users_from_data(users_data, output_callback)
        
        # Seed todos using shared utility
        self.stdout.write(self.style.SUCCESS('\n=== Seeding Todos ==='))
        todo_success, todo_errors = seed_todos_from_data(todos_data, output_callback)
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {user_success} created, {user_errors} errors'))
        self.stdout.write(self.style.SUCCESS(f'Todos: {todo_success} created, {todo_errors} errors'))
        self.stdout.write(self.style.SUCCESS('\n✓ Seeding complete!'))