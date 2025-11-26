"""
Django Management Command: seed_all
Run with: python manage.py seed_all

This command acts as an orchestrator that can call other seeding methods
to avoid code duplication. It can use:
- Django script functions (Method 3)
- Fixtures (Method 4)
- Other management commands
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import json
from pathlib import Path

# Import shared seeding utilities
from .seeding_utils import seed_users_from_data, seed_todos_from_data

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


class Command(BaseCommand):
    """
    Orchestrator command that can use different seeding methods.
    """
    
    help = 'Seeds the database using various methods (script functions, fixtures, or other commands)'
    
    def add_arguments(self, parser):
        """
        Add command-line arguments for different seeding methods.
        """
        parser.add_argument(
            '--method',
            type=str,
            choices=['script', 'fixtures', 'command', 'all'],
            default='script',
            help='Seeding method to use: script (Django script functions), fixtures (load fixtures), command (call seed_todos), or all (try all methods)'
        )
        parser.add_argument(
            '--users-file',
            type=str,
            default=None,
            help='Path to users JSON file (for script method, default: scripts/seeding/mock_data/users.json)'
        )
        parser.add_argument(
            '--todos-file',
            type=str,
            default=None,
            help='Path to todos JSON file (for script method, default: scripts/seeding/mock_data/todos.json)'
        )
        parser.add_argument(
            '--fixture-name',
            type=str,
            default=None,
            help='Fixture name to load (for fixtures method, e.g., initial_users)'
        )
    
    def handle(self, *args, **options):
        """
        Main method that routes to different seeding methods.
        """
        method = options['method']
        
        if method == 'script' or method == 'all':
            self._seed_via_script(options)
        
        if method == 'fixtures' or method == 'all':
            self._seed_via_fixtures(options)
        
        if method == 'command' or method == 'all':
            self._seed_via_command(options)
    
    def _seed_via_script(self, options):
        """
        Seed using Django script functions (Method 3).
        Reuses the logic from seed_script_django_script.py
        """
        self.stdout.write(self.style.SUCCESS('\n=== Seeding via Django Script Functions ==='))
        
        # Get file paths
        users_file = options.get('users_file') or PROJECT_ROOT / 'scripts' / 'seeding' / 'mock_data' / 'users.json'
        todos_file = options.get('todos_file') or PROJECT_ROOT / 'scripts' / 'seeding' / 'mock_data' / 'todos.json'
        
        # Load JSON data
        try:
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
            
            # Use the shared functions
            self.stdout.write(self.style.SUCCESS('\n--- Seeding Users ---'))
            user_success, user_errors = seed_users_from_data(users_data, output_callback)
            
            self.stdout.write(self.style.SUCCESS('\n--- Seeding Todos ---'))
            todo_success, todo_errors = seed_todos_from_data(todos_data, output_callback)
            
            # Summary
            self.stdout.write(self.style.SUCCESS(f'\n--- Summary ---'))
            self.stdout.write(self.style.SUCCESS(f'Users: {user_success} created, {user_errors} errors'))
            self.stdout.write(self.style.SUCCESS(f'Todos: {todo_success} created, {todo_errors} errors'))
            
            self.stdout.write(self.style.SUCCESS('\n✓ Script seeding complete!'))
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'✗ File not found: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error during script seeding: {e}'))
    
    def _seed_via_fixtures(self, options):
        """
        Seed using Django fixtures (Method 4).
        Calls Django's loaddata command.
        """
        self.stdout.write(self.style.SUCCESS('\n=== Seeding via Fixtures ==='))
        
        fixture_name = options.get('fixture_name')
        
        if fixture_name:
            # Load specific fixture
            try:
                call_command('loaddata', fixture_name, verbosity=1)
                self.stdout.write(self.style.SUCCESS(f'✓ Loaded fixture: {fixture_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error loading fixture {fixture_name}: {e}'))
        else:
            # Load default fixtures in order
            fixtures = ['users_data', 'todos_data']  # Load users first, then todos
            
            for fixture in fixtures:
                try:
                    call_command('loaddata', fixture, verbosity=1)
                    self.stdout.write(self.style.SUCCESS(f'✓ Loaded fixture: {fixture}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Error loading fixture {fixture}: {e}'))
            
            self.stdout.write(self.style.SUCCESS('\n✓ Fixture seeding complete!'))
    
    def _seed_via_command(self, options):
        """
        Seed by calling another management command (seed_todos).
        This shows how commands can call other commands.
        """
        self.stdout.write(self.style.SUCCESS('\n=== Seeding via Management Command ==='))
        
        try:
            # Call the seed_todos command
            call_command('seed_todos', verbosity=1)
            self.stdout.write(self.style.SUCCESS('\n✓ Command seeding complete!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error calling seed_todos command: {e}'))

